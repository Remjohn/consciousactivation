# No Real Render in V1

V1 explicitly blocks:

```text
Remotion calls
FFmpeg calls
subprocess runtime calls
provider calls
real media rendering
```

Real rendering belongs in a later Remotion/FFmpeg adapter bundle.
