# v4 界面截图与历史会话

本版截图来源为用户提供的 `长截图2.jpeg`，对应 2026-10-17 的历史会话。与 v3 不同，本次工作台概览、会话摘要、地图显示均来自同一张新长截图。

| 页面用途 | 文件 |
| --- | --- |
| 工作台概览 | `workbench-overview-v4.webp` |
| 完整长图（可滚动） | `workbench-full-v4.webp` |
| 会话结果摘要片段 | `agent-session-summary-v4.webp` |
| 地图预览局部 | `map-preview-detail-v4.webp` |
| 完整地图面板 | `map-preview-ui-v4.webp` |

会话编号采用不透明矩形遮挡。除此之外仅作固定裁剪，没有修改原截图中的文字、success 状态、pending 提示、图层或红色候选掩膜。原截图及原始会话归档均不进入站点。

截图中的预览请求 pending 是回复生成时的记录；截图的地图面板同时可见候选掩膜。保留原文，不将其涂改为其他状态。

## 配套会话的使用

读取 `.chat` 中 5 份实际工具返回，并与 `.tools.json` 中的 `tool_end` 事件核对：

1. 事件前影像获取：success，14 通道。
2. 事件后影像获取：success，14 通道。
3. 双时相组合：success，26 通道。
4. `run_landslide_detection`：success，ECI exit_code=0，推理输入 409 × 341、26 通道。
5. 预览请求：success；截图中可见红色候选掩膜。

网页只展示这些白名单字段的简短表格，记录在 `assets/SESSION_EVIDENCE_20261017.json`；原始输入坐标、路径、会话令牌、原始日志和归档不公开。摘要不构成模型精度、当前在线状态或所有镜像版本的验收证明。

原有静态 TIFF 案例区使用此前提供的 399 × 327 输入与对应结果，属于另一组素材。不能将其冒认为本次 409 × 341 输入的结果，也不将其他历史截图拼接到当前会话。

## 维护

截图路径与图注位于 `content.json → media`；界面区与会话表位于 `content.json → ui`。`fullSrc` 控制放大图，`scrollFull: true` 支持长图滚动。截图处理矩形和源文件 SHA-256 见 `assets/UI_PROCESSING.json`。
