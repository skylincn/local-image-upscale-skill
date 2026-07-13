---
name: local-image-upscale
description: Local-first image upscaling and restoration for 2K/4K output. Use when users ask to enlarge, sharpen, denoise, restore, or refine images without relying on Dreamina/Jimeng API; supports photos, portraits, products, anime, and text-heavy images with conservative model selection and explicit quality limits.
---

# 本地高清图片修复技能

Use a dedicated super-resolution backend for the base enlargement. On macOS, prefer the bundled UpScayl binary inside `/Applications/Upscayl.app`; do not require the GUI to be opened. Do not use GPT Image 2 as the default upscaler: generative editing may redraw faces, products, logos, or text.

## Workflow

1. Inspect the input format, pixel dimensions, color mode, and whether it contains a face, product, illustration, or dense text.
2. Inspect available local backends with `scripts/check_backends.py` before choosing a command. The detector checks both PATH commands and the standard macOS UpScayl app bundle.
3. For a local upscale, run `scripts/upscale.py INPUT OUTPUT --mode MODE --scale 2 --json`. Use its JSON result as the machine-readable execution record.
4. Select the least destructive backend:
   - `Real-ESRGAN` general/photo model for photographs, landscapes, and products.
   - `Real-ESRGAN` anime model for anime and illustrations.
   - `SwinIR` or high-quality classical resize for screenshots, documents, logos, and dense text.
   - Add `GFPGAN` or `CodeFormer` only for portraits that need face restoration; keep face restoration conservative.
5. Prefer 2x first. Apply a second stage only when the result still needs to reach 2K or 4K and the source has enough information.
6. Validate output dimensions, file readability, visual artifacts, faces, edges, logos, and text. Report when details were reconstructed rather than recovered.
7. Use GPT Image 2 only as an optional second pass for requested local repairs, masking, background cleanup, object retouching, reference-image generation, or style fusion.

## Backend Rules

- Never claim a stable 4K result when no dedicated super-resolution backend is installed.
- Never silently send user images to a cloud API. Ask for permission before using any external service.
- Preserve the original file and write outputs to a new path with a clear suffix such as `_2x` or `_4k`.
- Keep PNG for screenshots, text, and graphics; use high-quality JPEG or WebP for photographic output when size matters.
- Do not promise recovery of information absent from a severely blurred or tiny source.

## Model Selection

| Input | First choice | Avoid |
| --- | --- | --- |
| Photo, landscape, product | Real-ESRGAN general | Full-image generative redraw |
| Portrait | Real-ESRGAN, optional conservative GFPGAN/CodeFormer | Aggressive face restoration |
| Anime, illustration | Real-ESRGAN anime | Photo-only model |
| Screenshot, document, logo, UI | SwinIR or Lanczos/Sinc | Generative edit, which can alter text |

## References

Read [references/backend-notes.md](references/backend-notes.md) when installing or selecting a backend. Run `scripts/check_backends.py --json` when machine capability needs to be reported precisely. For this Mac, prefer the detected `upscayl_app_bin` path with `-i`, `-o`, `-s`, `-m`, and `-n` options.
