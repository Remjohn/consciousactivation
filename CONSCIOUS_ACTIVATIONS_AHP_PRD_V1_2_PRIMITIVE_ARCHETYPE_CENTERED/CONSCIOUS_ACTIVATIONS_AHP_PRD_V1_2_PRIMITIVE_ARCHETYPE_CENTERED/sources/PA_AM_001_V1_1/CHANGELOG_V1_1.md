# PA-AM-001 V1.1 Change Log

## Corrected product ownership

- Moved all GNM implementation ownership to the Visual Asset Editor.
- Removed GNM runtime and control generation from Interview Expression.
- Removed the proposed Pipeline-owned GNM package.
- Preserved only optional downstream communication:
  Interview Expression may produce an Expression Moment or Asset Package Spec; the
  Pipeline may later create a Visual Asset Demand; VAE independently decides whether
  to use GNM.

## Corrected parallel paths

- Lane D now owns VAE core with explicit GNM exclusions.
- Lane F now exclusively owns VAE GNM and GNM-specific ComfyUI paths.
- Lane E is explicitly bound to the existing Interview Expression product and is
  prohibited from creating another product root.
- Shared exports, dependency files, source registries, and status files remain
  integrator-only.

## Corrected GNM purpose

GNM is now defined as:

```text
main-avatar facial geometry spine
+ controllable expression/pose/gaze reference generator
+ ComfyUI conditioning source
```

It is not:

```text
Interview Expression engine
Pipeline core runtime
complete avatar identity authority
full-body avatar system
```

## Corrected implementation sequence

The deterministic GNM baseline comes first. A future Programmed Model may translate
bounded expression language into named GNM controls and bounded residuals only after
the baseline and data are available.
