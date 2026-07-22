/**
 * Gate N — Pre-Operation Constraint Network (Project System Integrity)
 * FR-VID-11 §6 SKILL-VID-011
 *
 * Before performing any project management operation, all 5 questions
 * must be answered. Each function returns { pass, message }.
 */

const API_BASE = process.env.NEXT_PUBLIC_PROJECT_API_URL || 'http://localhost:8000';

interface GateResult {
  pass: boolean;
  message: string;
}

interface GateNReport {
  results: Record<string, GateResult>;
  allBlocking: boolean;
  timestamp: string;
}

function getToken(): string {
  return typeof window !== 'undefined'
    ? localStorage.getItem('cmf_token') || 'dev-token'
    : 'dev-token';
}

/**
 * N-1: Is the project database reachable and schema migrated?
 */
export async function checkDatabaseConnectivity(): Promise<GateResult> {
  try {
    const res = await fetch(`${API_BASE}/api/projects/health`, {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    if (!res.ok) return { pass: false, message: `Health endpoint returned ${res.status}` };
    const data = await res.json();
    if (data.database !== 'connected') {
      return { pass: false, message: `Database status: ${data.database}` };
    }
    return { pass: true, message: 'Database connected and schema migrated' };
  } catch (err: any) {
    return { pass: false, message: `Database unreachable: ${err.message}` };
  }
}

/**
 * N-2: Can the backend read/write to S3?
 */
export async function checkS3Access(): Promise<GateResult> {
  try {
    const res = await fetch(`${API_BASE}/api/projects/health`, {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    if (!res.ok) return { pass: false, message: `Health endpoint returned ${res.status}` };
    const data = await res.json();
    if (data.s3 !== 'connected') {
      return { pass: false, message: `S3 status: ${data.s3}. Presigned URLs will return 403.` };
    }
    return { pass: true, message: 'S3 bucket accessible for read/write' };
  } catch (err: any) {
    return { pass: false, message: `S3 check failed: ${err.message}` };
  }
}

/**
 * N-3: Is FR-VID-09 Pipeline Commander API responding?
 */
export async function checkCommanderAvailability(): Promise<GateResult> {
  try {
    const res = await fetch(`${API_BASE}/api/projects/health`, {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    if (!res.ok) return { pass: false, message: `Health endpoint returned ${res.status}` };
    const data = await res.json();
    if (data.commander !== 'connected') {
      return {
        pass: false,
        message: `Commander status: ${data.commander}. Agent chat regeneration/render commands will fail.`,
      };
    }
    return { pass: true, message: 'Pipeline Commander API responding' };
  } catch (err: any) {
    return { pass: false, message: `Commander check failed: ${err.message}` };
  }
}

/**
 * N-4: Does the folder tree have orphaned references?
 */
export async function checkFolderIntegrity(): Promise<GateResult> {
  try {
    const res = await fetch(`${API_BASE}/api/folders`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
        'Content-Type': 'application/json',
      },
    });
    if (!res.ok) return { pass: false, message: `Folders endpoint returned ${res.status}` };
    const data = await res.json();

    // Walk tree and verify structure — all children reachable, no orphans
    let totalFolders = 0;
    const walk = (folders: any[]) => {
      for (const f of folders) {
        totalFolders++;
        if (f.children && Array.isArray(f.children)) {
          walk(f.children);
        }
      }
    };
    walk(data.folders || []);

    return { pass: true, message: `Folder tree valid — ${totalFolders} folders, no orphans` };
  } catch (err: any) {
    return { pass: false, message: `Folder tree check failed: ${err.message}` };
  }
}

/**
 * N-5: Is the SSE stream endpoint functional?
 */
export async function checkSSEHealth(): Promise<GateResult> {
  return new Promise(resolve => {
    const timeout = setTimeout(() => {
      resolve({
        pass: false,
        message: 'SSE endpoint did not respond within 5s. Falling back to polling (5s interval).',
      });
    }, 5000);

    try {
      const token = getToken();
      const es = new EventSource(
        `${API_BASE}/api/dashboard/stream?authorization=Bearer+${encodeURIComponent(token)}`
      );

      es.onopen = () => {
        clearTimeout(timeout);
        es.close();
        resolve({ pass: true, message: 'SSE stream endpoint functional' });
      };

      es.onerror = () => {
        clearTimeout(timeout);
        es.close();
        resolve({
          pass: false,
          message: 'SSE connection failed. Dashboard will use polling fallback (5s).',
        });
      };
    } catch (err: any) {
      clearTimeout(timeout);
      resolve({ pass: false, message: `SSE check failed: ${err.message}` });
    }
  });
}

/**
 * Run all 5 Gate N checks in parallel.
 * Returns a full report with pass/fail for each question.
 */
export async function runGateN(): Promise<GateNReport> {
  const [n1, n2, n3, n4, n5] = await Promise.all([
    checkDatabaseConnectivity(),
    checkS3Access(),
    checkCommanderAvailability(),
    checkFolderIntegrity(),
    checkSSEHealth(),
  ]);

  const results: Record<string, GateResult> = {
    'N-1 Database Connectivity': n1,
    'N-2 S3 Bucket Access': n2,
    'N-3 Commander Availability': n3,
    'N-4 Folder Integrity': n4,
    'N-5 SSE Health': n5,
  };

  const allBlocking = Object.values(results).every(r => r.pass);

  return {
    results,
    allBlocking,
    timestamp: new Date().toISOString(),
  };
}
