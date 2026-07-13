# 本地化图片超分修复

`local-image-upscale` 是一个面向 Codex / xiaow 的本地图片高清放大与修复 skill。

它优先调用 macOS UpScayl 应用内置的 Real-ESRGAN CLI。基础放大与生成式改图分开处理：UpScayl 负责稳定的 2K/4K 高清放大，GPT Image 2 可选用于局部修复、mask 改图、参考图生图和风格融合。

文档使用上游模型名称，不使用内部渠道名称。当前公开版本统一使用 GPT Image 2。

## 功能

- 照片、人物、商品、风景、动漫和插画的 2K/4K 放大
- 根据图片类型选择更稳妥的本地模型
- 保留原图并生成新的输出文件
- 检测本机是否安装 UpScayl 和可用 CLI
- 明确区分“真实超分放大”和“AI 重绘修复”

## 安装

```bash
git clone https://github.com/skylincn/local-image-upscale-skill.git \
  ~/.codex/skills/local-image-upscale
```

安装 UpScayl 后，skill 会自动寻找：

```text
/Applications/Upscayl.app/Contents/Resources/bin/upscayl-bin
/Applications/Upscayl.app/Contents/Resources/models
```

检查本地后端：

```bash
python3 ~/.codex/skills/local-image-upscale/scripts/check_backends.py
```

## Local CLI

The bundled wrapper selects a conservative UpScayl model and emits a JSON execution record:

```bash
python3 ~/.codex/skills/local-image-upscale/scripts/upscale.py \
  input.jpg output.png \
  --mode portrait --scale 2 --json
```

Supported modes are `photo`, `portrait`, `product`, `general`, `sharp`, `anime`, `illustration`, and `text`. The wrapper never uploads the image and never overwrites the input.

## 使用

在 Codex 或 xiaow 中调用：

```text
使用 $local-image-upscale 处理这张图片，输出 4K，尽量保持人物和原图构图不变。
```

也可以指定类型：

```text
使用 $local-image-upscale，以人像模式放大到 2K。
使用 $local-image-upscale，以商品模式处理这张产品图。
使用 $local-image-upscale，以动漫模式放大这张插画。
```

## 模型建议

| 图片类型 | 推荐模型 |
| --- | --- |
| 照片、人像、商品 | `high-fidelity-4x` / `ultramix-balanced-4x` |
| 通用锐化 | `ultrasharp-4x` |
| 动漫、插画 | `digital-art-4x` |
| 保守照片增强 | `remacri-4x` |

小尺寸图片优先 2x 放大，确认结果后再继续到 4K，避免一次放大造成假细节和伪影。

## 能力边界

| 需求 | 处理方式 |
| --- | --- |
| 稳定高清放大 | UpScayl / Real-ESRGAN |
| 局部修复、mask 改图 | GPT Image 2 |
| 参考图生图、风格融合 | GPT Image 2 |
| 局部改图 | GPT Image 2 |

严重模糊或尺寸过小的图片，模型只能重建可能的细节，不能保证恢复真实信息。文字、logo、二维码和 UI 截图应优先使用保守放大，并进行人工检查。

## 目录结构

```text
local-image-upscale-skill/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/openai.yaml
├── references/backend-notes.md
└── scripts/
    ├── check_backends.py
    └── upscale.py
```

## License

MIT License，详见 [LICENSE](LICENSE)。
