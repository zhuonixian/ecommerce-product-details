# 成品与源文件清单

由于当前 GitHub 连接的写入接口只支持 UTF-8 文本文件，本次生成的二进制图片、PDF 与 ZIP 暂未写入 Git 仓库。完整项目包已保存在本次交付中，后续可通过 Git CLI、Git LFS 或 GitHub Release 上传。

## 成品包

| 文件 | 大小 | SHA-256 |
| --- | ---: | --- |
| 00-甘南风干牦牛肉干-详情页-9x16.zip | 17,666,239 B | `58c5402c8107979acc42bacb5f2af4de4fcb35a6ff61dc5848cc3ae8f62fb6a8` |
| 01-青稞桑葚5款商品详情页-9x16.zip | 46,001,426 B | `d8ea637d98f36a0663f36445b7261a7e83248b726975837633b6ad5a999bce5a` |
| 02-红枣枸杞5款商品详情页-9x16.zip | 46,202,099 B | `2422b4eb7d9cbf6da150d63be4f057d27e088077c8d890f596c52f939294b418` |

## 输入与参考

| 文件 | SHA-256 |
| --- | --- |
| 2026-price-list.pdf | `51932536fe4f3e37be48430847082e248a0e0d12b6f6c74cbdcdb62ca7355e03` |
| style-reference.jpeg | `5a91f96be6b1257a73f50d68dfe744396c182e9518cda04c6a72c9437970c74b` |

## 建议上传方式

大文件建议作为 GitHub Release 附件保存；如果需要在 Git 中版本化图片，使用 Git LFS 管理 `*.png`、`*.jpg`、`*.pdf` 和 `*.zip`。
