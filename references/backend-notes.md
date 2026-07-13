# Backend Notes

The skill is local-first and uses the locally available backend configuration.

Preferred options:

- Real-ESRGAN: general-purpose 2x/4x super-resolution; use an NCNN/Vulkan or Python implementation depending on what is installed.
- SwinIR: useful when denoising and faithful restoration matter more than aggressive texture synthesis.
- GFPGAN or CodeFormer: optional portrait-face restoration only, with conservative settings.
- ImageMagick or Pillow high-quality resize: deterministic fallback for text-heavy images when no AI backend is installed.

The fallback resize improves dimensions but cannot invent missing detail. It should be reported as resize-only, not AI restoration.

On macOS, also check `/Applications/Upscayl.app/Contents/Resources/bin/upscayl-bin`. The installed UpScayl app bundles models and a command-line binary. Its useful options include `-i` input, `-o` output, `-s` output scale, `-r` target resize, `-m` model directory, and `-n` model name. Prefer the bundled model directory from the same app bundle so the binary and weights stay compatible.

Do not install packages or download model weights without explicit user approval.
