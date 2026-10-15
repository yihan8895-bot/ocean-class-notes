# 海洋课堂笔记 / Ocean Classroom Notes

公开的中英文对照物理海洋学资料库，含课堂问答、南海海洋热浪分析、EOF 图表与动画，以及地转流专题。This public bilingual physical-oceanography library contains classroom answers, South China Sea marine-heatwave analysis, EOF figures and animation, and a geostrophic-flow atlas.

- 网站 / Website: https://yihan8895-bot.github.io/ocean-class-notes/
- 资料 / Articles: `content.json` and `content/additions.json`
- 图片与动画 / Images and animation: `assets/`
- 地转流数据分析 / Geostrophic data analysis: `analysis/geostrophic_scs_2016_2025.m`

地转流专题使用本地 NOAA OISST v2.1 南海子集生成 2016–2025 年温度锋面图。脚本只把 SST 梯度作为温度锋面指标，不把它当作海面高度梯度或绝对地转流。The geostrophic atlas uses a local NOAA OISST v2.1 South China Sea subset to generate 2016–2025 thermal-front figures. The script treats SST gradients as a thermal-front metric, not as sea-surface-height gradients or absolute geostrophic currents.

## 如何添加课堂内容 / How to add content

1. 打开网站的「添加内容 / Add Content」页面，填写标题、分类、简介和正文。   Open the site's Add Content page and fill in title, category, summary and body.
2. 下载生成的 `additions.json`，在 GitHub 的 `https://github.com/yihan8895-bot/ocean-class-notes/upload/main/content` 页面上传，提交到 `main`。   Download the generated file, upload it to `https://github.com/yihan8895-bot/ocean-class-notes/upload/main/content`, and commit it to `main`.
3. GitHub Pages 从 `main` 分支根目录发布。提交完成后等待 Pages 更新。   GitHub Pages publishes from the root of `main`; allow time for the update.

文章正文请用空行分段。文章和配图均公开可见，提交前请不要包含个人隐私。Separate body paragraphs with blank lines. Articles and images are public; remove personal information before committing.

## 来源与许可 / Sources and licensing

方法与数据来源见各篇文章。课堂图与本地研究输出可能包含用户或第三方素材；公开可读不代表这些素材自动获得再利用许可。Methods and data sources are linked in each article. Classroom figures and local research outputs may contain user or third-party material; public visibility does not imply a reuse licence for those assets.
