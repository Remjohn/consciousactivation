from __future__ import annotations
from pathlib import Path
from typing import Any, Mapping
from ca_contracts import bytes_sha256

class SimplePdfExporter:
    def export(self, composition: Mapping[str,Any], destination: str|Path) -> Path:
        width=composition['canvas']['width_px'];height=composition['canvas']['height_px']
        objects=[]
        def add(data:bytes)->int: objects.append(data);return len(objects)
        page_ids=[];content_ids=[]
        font_id=add(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
        for page in composition['pages']:
            commands=[]
            bg=composition['canvas']['background_rgb'];commands.append(f"{bg[0]/255:.4f} {bg[1]/255:.4f} {bg[2]/255:.4f} rg 0 0 {width} {height} re f")
            for e in page['elements']:
                b=e['bbox'];x=b['x']*width//1_000_000;y=height-(b['y']+b['height'])*height//1_000_000;w=b['width']*width//1_000_000;h=b['height']*height//1_000_000
                c=e['background_rgb'];commands.append(f"{c[0]/255:.4f} {c[1]/255:.4f} {c[2]/255:.4f} rg {x} {y} {w} {h} re f")
                if e['text']!='NOT_APPLICABLE':
                    fg=e['foreground_rgb'];safe=e['text'].replace('\\','\\\\').replace('(','\\(').replace(')','\\)')[:600]
                    commands.append(f"BT /F1 {e['font_size_px']} Tf {fg[0]/255:.4f} {fg[1]/255:.4f} {fg[2]/255:.4f} rg {x+4} {y+h-e['font_size_px']-4} Td ({safe}) Tj ET")
            stream='\n'.join(commands).encode('latin-1','replace');content_ids.append(add(b'<< /Length '+str(len(stream)).encode()+b' >>\nstream\n'+stream+b'\nendstream'))
            page_ids.append(None)
        pages_id=len(objects)+len(page_ids)+1
        for i,content_id in enumerate(content_ids):
            page_ids[i]=add(f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {width} {height}] /Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>".encode())
        kids=' '.join(f'{pid} 0 R' for pid in page_ids);actual_pages=add(f'<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>'.encode())
        assert actual_pages==pages_id
        catalog_id=add(f'<< /Type /Catalog /Pages {pages_id} 0 R >>'.encode())
        out=bytearray(b'%PDF-1.4\n');offsets=[0]
        for i,obj in enumerate(objects,1): offsets.append(len(out));out.extend(f'{i} 0 obj\n'.encode());out.extend(obj);out.extend(b'\nendobj\n')
        xref=len(out);out.extend(f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode())
        for off in offsets[1:]:out.extend(f'{off:010d} 00000 n \n'.encode())
        out.extend(f'trailer\n<< /Size {len(objects)+1} /Root {catalog_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
        path=Path(destination);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(out);return path
