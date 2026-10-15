# 图片与截图维护

本版所有页面素材均已替换为真实影像、模型结果或界面截图，不再展示业务图片占位。架构图仍为据工程关系绘制的结构示意。

| 编号 | 用途 | 内容源与文件 |
| --- | --- | --- |
| P01 | 工作台界面概览与长图放大 | `media.workbench`；`workbench-overview.webp` / `workbench-full.webp` |
| P02 | 事件前后真彩色 | `media.inputs`；`temporal-inputs.webp` |
| P03 | 滑坡结果与对比 | `media.landslide`、`comparisons.landslide`；`landslide-*.webp/png` |
| P04 | 裂缝结果与对比 | `media.crack`、`comparisons.crack`；`crack-*.webp/png` |
| P05 | 真实工具调用片段 | `media.trace`；`agent-tool-trace.webp` |
| P06 | 真实地图成果预览 | `media.mapPreview`；`map-preview-detail.webp` / `map-preview-ui.webp` |
| 首页 | 滑坡叠加成果 | `media.hero`；`landslide-overlay.webp` |

界面截图说明见 `UI_SCREENSHOTS.md`。TIFF 导图、26 通道映射和滑坡网格差异见 `DEMO_ASSETS.md`。

更换真实案例时，输入图、叠加图和二值图必须同范围同画布；更新 `comparisons` 中的路径与尺寸。更换截图时可用 `fullSrc` 提供放大图，长图设 `scrollFull: true`。修改后使用 Actions 发布，或运行 `python scripts/build.py` 后上传生成首页。

本版不展示视频或视频占位；保留的在线体验入口属于独立服务跳转，与视频无关。
