# FFmpeg Finish Plan

The FFmpeg finish job owns:

```text
input file ref
output file ref
codec
filters
loudness / scale / mux hints
```

It must not call providers and must not execute unless runtime gates pass.
