# 从第二版更新到第三版

## 本次变化

- 补入工作台概览、完整长截图、真实工具调用片段和地图成果预览。
- 图片放大支持长截图滚动查看；原有滑坡 / 裂缝拖动对比与通道表保留。
- 移除整个视频模块和“录屏待补充”等占位文案。
- 在线交互入口仍可独立配置。旧配置中的 `video` 字段被忽略，不会重新启用视频。

## 覆盖更新

将下列内容覆盖到现有克隆仓库根目录：

- `index.html`、`content.json`、`README.md`、`UPDATE_FROM_V2.md`
- `assets/`、`css/`、`js/`、`scripts/`、`docs/`

保留 `.git/`、`.github/workflows/pages.yml` 和自己的 `config/site.json`。无需修改 Pages 设置或重新克隆。若你自行修改过页面文字，请先保留原 `content.json`，再合并本版内容。

```bash
git add .
git commit -m "Add workbench screenshots and remove video placeholder"
git push origin main
```

本包没有访问或推送你的 GitHub 仓库；提交后等待现有 Actions 发布即可。实际浏览器和线上效果仍需在最终网址核对。
