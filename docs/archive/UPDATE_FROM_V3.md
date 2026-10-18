# 从 v3 更新到 v4

## 本版更新

- 使用 `长截图2.jpeg` 替换此前工作台长图与会话片段；完整长图、概览、会话摘要和地图裁图来自同次截图。
- 增加可展开的 2026-10-17 历史会话摘要，核对了 5 次工具返回的 success、26 通道组合与 ECI exit_code=0。原始归档不进入网站。
- 在线入口设为 `http://121.40.114.105:7860`。顶部“在线体验”和底部按钮均新窗口打开，不嵌入、不自动请求业务服务。
- 导航文字从桌面 12 px 提升到 16 px，窄屏为 14 px；保留原导航栏高度。栏目标题与正文适度增大。
- 滑坡 / 裂缝静态对比、26 通道表与视频移除状态保持。

## 重要：这次需要更新在线入口配置

v3 曾建议保留原 `config/site.json`。本次新增了在线地址，**必须同时更新该配置和 `js/app.js`**；只替换页面或只保留旧配置，不会出现新的入口。

把本包的 `index.html`、`content.json`、`css/`、`js/`、`assets/`、`scripts/`、`docs/`、`README.md` 和 `UPDATE_FROM_V3.md` 覆盖到已有仓库根目录。保留 `.git/` 和原 Pages 工作流。

若原配置没有自定义其他链接，直接覆盖本包 `config/site.json`。若需保留自己的 `links`，仅把 `demo` 对象改为：

```json
{
  "enabled": true,
  "url": "http://121.40.114.105:7860",
  "allowHttp": true,
  "deploymentMode": "eci",
  "statusText": "在线体验入口已配置",
  "lastVerifiedAt": null
}
```

这里是 `demo` 对象，不是整个配置文件。`lastVerifiedAt` 为空表示没有伪造人工核实时间；仍显示项目本人明确提供的入口。若以后改为 HTTPS，可将 `allowHttp` 改为 `false`。

## 提交

在已有克隆仓库中执行：

```powershell
git status -sb
git add .
git commit -m "Update workbench evidence and enable live demo link"
git push origin main
```

如果之前已经设置仓库代理，可继续沿用；本包不会修改 Git 的代理或登录设置。

## 验证范围

已核对原始会话结构化状态、截图与公开副本、资源引用、配置与外链逻辑；没有把原始日志或原截图带入公开包。历史记录证明当时的执行返回，不能代替当前服务探活。

当前环境未执行实际浏览器 / 线上发布验证，也没有访问该业务服务来提交任务或探测健康状态。上传后请在最终网址确认字体、截图与新窗口跳转。
