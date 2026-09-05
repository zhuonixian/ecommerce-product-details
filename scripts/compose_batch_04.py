from pathlib import Path
import importlib.util

ROOT = Path('/workspace/scratch/9d2cf2528637')
spec = importlib.util.spec_from_file_location('base_batch', ROOT / 'tmp/imagegen/compose_next_batch.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

bg_slices = ROOT / 'generated_images/exec-d9dad80c-f9c3-42a9-8aa8-693eada6086e.png'
bg_crisp = ROOT / 'generated_images/exec-ef07e2ad-53bd-44d4-908e-14540681474a.png'
bg_walnut = ROOT / 'generated_images/exec-fabb1d42-d0eb-4e8d-aa26-6485c2ce589a.png'
bg_goji_gift = ROOT / 'generated_images/exec-ee4fc1f3-f351-4adc-a6c5-14af60dace93.png'
bg_walnut_gift = ROOT / 'generated_images/exec-81fbc42b-8662-4cba-aa3e-d631b04e2e7e.png'

b.PRODUCTS = [
{
 'key':'date-slices','dir':'crispy-date-slices-detail','name':'香脆枣片','eyebrow':'红枣切片轻食','tagline':'薄脆枣片 / 自然枣香',
 'product_image':ROOT/'tmp/pdfs/extracted-images/img-015.png','hero':bg_slices,'process':bg_slices,'scene':bg_slices,
 'dark':(110,45,38),'dark2':(58,20,19),'accent':(225,176,91),'cream':(255,244,224),'ink':(94,43,31),
 'badges':['灰枣原料','去核切片','酥脆即食'],
 'source_title':'优质灰枣 自然风干','source_subtitle':'甄选枣果 切片烘制','source_statement':['精选自然风干灰枣','枣香浓郁 薄片酥脆'],
 'source_features':[('自然风干','灰枣原料'),('层层挑选','完整分选'),('无核切片','食用方便')],
 'process_steps':[('原料分选','挑选灰枣'),('清洗去核','整理枣果'),('均匀切片','薄片成型'),('分段烘制','酥脆完成')],
 'detail_title':'片片轻脆 枣香自然','detail_subtitle':'圆形切面 清晰可见','detail_features':[('薄片形态','轻脆易食'),('枣香自然','甜润适口'),('去核处理','取食方便'),('干爽口感','开袋即食')],
 'spec_rows':[('产品类别','零食 / 枣片'),('产品规格','400g / 袋'),('主要原料','灰枣'),('加工特点','去核 / 切片 / 烘制'),('食用方式','即食 / 泡茶 / 煲汤')],
 'nutrition_title':'配料与营养说明','nutrition_body':['枣片配料与营养数值','请以实物包装标注为准'],
 'scene_title':'轻脆枣香 多种搭配','scene_subtitle':'即食 / 泡茶 / 煲汤 / 分享','scenes':[('开袋即食','轻脆枣香'),('温水泡茶','自然回甜'),('煲汤搭配','加入枣香'),('居家分享','老少同享')]
},
{
 'key':'crispy-dates','dir':'crispy-whole-dates-detail','name':'香酥脆枣','eyebrow':'整颗香酥脆枣','tagline':'整颗脆枣 / 酥脆香甜',
 'product_image':ROOT/'tmp/pdfs/extracted-images/img-016.png','hero':bg_crisp,'process':bg_crisp,'scene':bg_crisp,
 'dark':(89,48,25),'dark2':(45,23,12),'accent':(222,174,80),'cream':(255,246,223),'ink':(83,48,24),
 'badges':['优质灰枣','无核整枣','香酥不腻'],
 'source_title':'自然风干灰枣 精细挑选','source_subtitle':'整颗去核 保留枣香','source_statement':['精选自然风干灰枣','整颗香酥 枣味浓郁'],
 'source_features':[('优质灰枣','自然枣香'),('三级清洗','层层处理'),('人工挑选','品质分选')],
 'process_steps':[('灰枣甄选','层层分选'),('清洗去核','整枣处理'),('轻度油浸','中度脆制'),('充分沥油','香酥完成')],
 'detail_title':'整颗酥脆 香甜不腻','detail_subtitle':'外层香酥 内里轻脆','detail_features':[('整颗形态','饱满可见'),('无核处理','轻松取食'),('酥脆香甜','枣味保留'),('独立小袋','便于携带')],
 'spec_rows':[('产品类别','零食 / 脆枣'),('产品规格','500g / 袋'),('主要原料','灰枣'),('加工特点','去核 / 脆制 / 沥油'),('食用方式','开袋即食')],
 'nutrition_title':'配料与营养说明','nutrition_body':['油脂、配料与营养数值','请以实物包装标注为准'],
 'scene_title':'整颗轻脆 随时享用','scene_subtitle':'追剧 / 旅途 / 办公 / 分享','scenes':[('居家追剧','酥脆解馋'),('外出旅途','方便携带'),('办公加餐','随手取食'),('家庭分享','一起品尝')]
},
{
 'key':'date-walnut','dir':'date-walnut-detail','name':'枣夹核桃','eyebrow':'红枣核桃双料','tagline':'细腻红枣 / 酥香核桃',
 'product_image':ROOT/'tmp/pdfs/extracted-images/img-021.png','hero':bg_walnut,'process':bg_walnut,'scene':bg_walnut,
 'dark':(91,35,17),'dark2':(47,15,8),'accent':(225,171,76),'cream':(255,242,214),'ink':(87,42,22),
 'badges':['红枣果肉','核桃夹心','双重口感'],
 'source_title':'优质红枣 遇见核桃','source_subtitle':'两种原料 风味互补','source_statement':['红枣包裹酥香核桃','枣甜柔和 坚果香浓'],
 'source_features':[('优质红枣','细腻甜润'),('核桃仁','酥脆醇厚'),('双料搭配','层次丰富')],
 'process_steps':[('红枣甄选','清洗去核'),('核桃分选','准备核仁'),('手工夹心','双料结合'),('品质分选','完成封装')],
 'detail_title':'枣肉细腻 核桃酥香','detail_subtitle':'软糯与酥脆 一口融合','detail_features':[('红枣软糯','香甜细腻'),('核桃酥香','醇厚有层次'),('夹心饱满','切面可见'),('双重风味','甜香相融')],
 'spec_rows':[('产品类别','零食 / 干果'),('产品规格','500g / 袋'),('主要原料','红枣 / 核桃仁'),('产品形态','红枣夹核桃'),('食用方式','开袋即食')],
 'nutrition_title':'配料与营养说明','nutrition_body':['红枣与核桃仁具体含量','请以实物包装标注为准'],
 'scene_title':'双料枣香 日常分享','scene_subtitle':'茶点 / 办公 / 旅途 / 家庭','scenes':[('中式茶点','搭配香茶'),('办公加餐','软酥相伴'),('旅途补给','袋装方便'),('家庭分享','双料美味')]
},
{
 'key':'goji-gift','dir':'goji-gift-detail','name':'红枸杞礼盒','eyebrow':'红枸杞分享礼盒','tagline':'红润果粒 / 礼盒心意',
 'product_image':ROOT/'tmp/pdfs/extracted-images/img-020.png','hero':bg_goji_gift,'process':bg_goji_gift,'scene':bg_goji_gift,
 'dark':(128,24,15),'dark2':(67,8,7),'accent':(232,183,77),'cream':(255,246,219),'ink':(106,38,20),
 'badges':['红枸杞','600g礼盒','多样搭配'],
 'source_title':'红润枸杞 礼盒分享','source_subtitle':'干燥果粒 日常取用','source_statement':['甄选红润枸杞果粒','自然干香 多样搭配'],
 'source_features':[('红润果粒','外观自然'),('干燥处理','便于保存'),('礼盒包装','分享心意')],
 'process_steps':[('果实采收','适时采摘'),('分选清理','去除杂质'),('干燥处理','形成干果'),('礼盒装配','完整封装')],
 'detail_title':'粒粒红润 干香自然','detail_subtitle':'可泡饮 可煮粥 可入汤','detail_features':[('果粒红润','自然色泽'),('干香微甜','风味柔和'),('泡饮方便','温水舒展'),('多样搭配','粥汤皆宜')],
 'spec_rows':[('产品类别','零食 / 干果'),('产品规格','600g / 盒'),('产品形态','干燥枸杞'),('包装方式','礼盒装'),('食用方式','泡饮 / 煮粥 / 入汤')],
 'nutrition_title':'食用与营养说明','nutrition_body':['具体配料、营养数值与食用量','请以实物包装标注为准'],
 'scene_title':'礼盒心意 多样搭配','scene_subtitle':'赠礼 / 泡水 / 煮粥 / 煲汤','scenes':[('节日赠礼','红色心意'),('温水泡饮','果粒舒展'),('早餐煮粥','加入谷物'),('日常煲汤','丰富搭配')]
},
{
 'key':'date-walnut-gift','dir':'date-walnut-gift-detail','name':'枣夹核桃礼盒','eyebrow':'红枣核桃礼盒','tagline':'双料美味 / 礼盒分享',
 'product_image':ROOT/'tmp/pdfs/extracted-images/img-019.png','hero':bg_walnut_gift,'process':bg_walnut_gift,'scene':bg_walnut_gift,
 'dark':(111,18,16),'dark2':(57,6,7),'accent':(232,187,84),'cream':(255,243,216),'ink':(98,31,22),
 'badges':['红枣核桃','1kg礼盒','亲友分享'],
 'source_title':'红枣核桃 双料成礼','source_subtitle':'真材组合 一口双香','source_statement':['红枣果肉包裹核桃仁','枣香浓郁 核桃酥香'],
 'source_features':[('优质红枣','甜润细腻'),('核桃仁','酥香醇厚'),('礼盒包装','适合分享')],
 'process_steps':[('红枣处理','清洗去核'),('核桃分选','准备核仁'),('夹心成型','双料结合'),('礼盒装配','完整封装')],
 'detail_title':'甜润枣香 酥香核桃','detail_subtitle':'双重原料 风味层层展开','detail_features':[('枣肉软糯','香甜细腻'),('核桃酥香','醇厚有层次'),('夹心饱满','真材可见'),('礼盒分享','心意之选')],
 'spec_rows':[('产品类别','零食 / 干果'),('产品规格','1kg / 盒'),('主要原料','红枣 / 核桃仁'),('包装方式','礼盒装'),('食用方式','开盒即食')],
 'nutrition_title':'配料与营养说明','nutrition_body':['红枣与核桃仁具体含量','请以实物包装标注为准'],
 'scene_title':'双料成礼 分享心意','scene_subtitle':'节日 / 走亲 / 相聚 / 茶桌','scenes':[('节日赠礼','红色礼盒'),('走亲送礼','分享心意'),('家庭相聚','双料同享'),('茶桌分享','枣香核桃')]
}
]

b.OUT_ROOT = ROOT / 'output/imagegen/batch-04'

if __name__ == '__main__':
    b.main()
