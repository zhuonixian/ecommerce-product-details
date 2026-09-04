from pathlib import Path
import importlib.util
from PIL import Image

ROOT = Path('/workspace/scratch/9d2cf2528637')
spec = importlib.util.spec_from_file_location('base_batch', ROOT / 'tmp/imagegen/compose_next_batch.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

asset_dir = ROOT / 'tmp/imagegen/following5-assets'
asset_dir.mkdir(parents=True, exist_ok=True)

# Two package photos on PDF page 2 are flattened into the page; crop them at high quality.
page = Image.open(ROOT / 'tmp/pdfs/next5-pages/page-02.jpg').convert('RGB')
page.crop((914, 770, 1125, 975)).save(asset_dir / '奶芙枣-包装.jpg', quality=96)
page.crop((914, 970, 1125, 1200)).save(asset_dir / '芝麻枣夹核桃-包装.jpg', quality=96)

def product(**kwargs):
    return kwargs

bg_gift = ROOT / 'generated_images/exec-8d13cf10-e68a-43e3-949e-a21c3fbaa92c.png'
bg_milk = ROOT / 'generated_images/exec-493ee59a-07db-4824-9650-c653d68fee3c.png'
bg_sesame = ROOT / 'generated_images/exec-c868982e-ec98-4d3f-9be1-8c93b590f463.png'
bg_bar = ROOT / 'generated_images/exec-ff4f7120-a645-429b-ae44-7dfd621f839c.png'
bg_goji = ROOT / 'generated_images/exec-81f97ba8-8b57-416d-b734-95d21b343ecd.png'

b.PRODUCTS = [
product(key='date-gift', dir='premium-date-gift-detail', name='精品红枣礼盒', eyebrow='多味红枣组合礼盒', tagline='四款枣味 / 节日分享',
 product_image=ROOT/'tmp/pdfs/extracted-images/img-019.png', hero=bg_gift, process=bg_gift, scene=bg_gift,
 dark=(104,20,18), dark2=(55,8,8), accent=(230,187,87), cream=(255,245,220), ink=(92,33,22),
 badges=['四款组合','红枣风味','礼盒分享'],
 source_title='四款枣味 一盒相聚', source_subtitle='临泽小枣 / 临泽焦枣 / 鸡心脆枣 / 香脆枣片', source_statement=['精选多款枣制品','甜润与酥脆 丰富搭配'],
 source_features=[('临泽小枣','甘甜爽口'),('临泽焦枣','枣香浓郁'),('脆枣枣片','酥脆甜糯')],
 process_steps=[('原料甄选','挑选红枣'),('分类加工','形成多味'),('品质分选','组合入盒'),('礼盒装配','完整封装')],
 detail_title='一盒四味 丰富有层次', detail_subtitle='甜润 / 枣香 / 酥脆 / 软嫩', detail_features=[('临泽小枣','甘甜爽口'),('临泽焦枣','枣香温润'),('香脆枣片','酥脆甜糯'),('鸡心脆枣','酥脆里嫩')],
 spec_rows=[('产品类别','零食 / 干果'),('产品规格','1.6kg / 盒'),('组合单品','四款红枣制品'),('包装方式','组合礼盒'),('食用方式','开盒即食')],
 nutrition_title='组合资料说明', nutrition_body=['各单品配料与营养资料','请分别以实物包装标注为准'],
 scene_title='佳节心意 分享枣香', scene_subtitle='节日 / 送礼 / 家庭 / 相聚', scenes=[('节日赠礼','红色礼盒'),('走亲送礼','分享心意'),('家庭茶桌','四味同享'),('相聚分享','枣香相伴')]),
product(key='milk-date', dir='milk-nougat-date-detail', name='奶芙枣', eyebrow='奶香红枣夹心', tagline='红枣 / 奶芙 / 核桃仁',
 product_image=asset_dir/'奶芙枣-包装.jpg', hero=bg_milk, process=bg_milk, scene=bg_milk,
 dark=(119,39,24), dark2=(66,20,14), accent=(230,176,88), cream=(255,248,231), ink=(100,48,30), badges=['红枣夹心','奶香柔和','核桃搭配'],
 source_title='红枣奶芙 核桃相遇', source_subtitle='三重食材 带来丰富口感', source_statement=['红枣包裹柔软奶芙','加入烘焙核桃仁'],
 source_features=[('优质红枣','甜润枣香'),('奶芙夹心','奶味柔和'),('烘焙核桃','坚果香气')],
 process_steps=[('食材准备','红枣与核桃'),('奶芙制作','棉花糖与黄油'),('夹心组合','层次成型'),('独立装袋','便于分享')],
 detail_title='软糯枣香 奶香夹心', detail_subtitle='柔软奶芙与核桃颗粒 层次丰富', detail_features=[('枣香甜润','外层软糯'),('奶芙柔软','奶味纯正'),('核桃颗粒','坚果口感'),('甜度适中','风味相融')],
 spec_rows=[('产品类别','零食 / 干果'),('产品规格','245g / 袋'),('主要搭配','红枣 / 奶芙 / 核桃'),('包装方式','袋装'),('食用方式','开袋即食')],
 nutrition_title='配料与营养说明', nutrition_body=['含红枣、奶芙、核桃等原料','具体资料以实物包装为准'],
 scene_title='甜润一颗 随时分享', scene_subtitle='茶点 / 办公 / 旅途 / 家庭', scenes=[('午后茶点','奶香枣甜'),('办公加餐','轻松解馋'),('旅途携带','袋装方便'),('家庭分享','老少同享')]),
product(key='sesame-walnut-date', dir='sesame-walnut-date-detail', name='芝麻枣夹核桃', eyebrow='红枣核桃组合', tagline='红枣 / 核桃 / 芝麻',
 product_image=asset_dir/'芝麻枣夹核桃-包装.jpg', hero=bg_sesame, process=bg_sesame, scene=bg_sesame,
 dark=(83,35,17), dark2=(43,18,9), accent=(222,169,75), cream=(252,241,215), ink=(83,44,23), badges=['去核红枣','核桃夹心','芝麻添香'],
 source_title='红枣核桃 芝麻点香', source_subtitle='三种食材 一口多重口感', source_statement=['去核红枣夹入核桃','芝麻添香 风味更丰富'],
 source_features=[('优质红枣','甜润软糯'),('核桃仁','酥香饱满'),('芝麻添香','香气丰富')],
 process_steps=[('红枣去核','挑选处理'),('核桃准备','核仁分选'),('夹心组合','芝麻添香'),('独立包装','随取随享')],
 detail_title='枣软核桃酥 芝麻香', detail_subtitle='一颗一袋 随手享用', detail_features=[('枣肉软糯','甜润枣香'),('核桃酥香','颗粒饱满'),('芝麻增香','黑白相间'),('独立小袋','随身方便')],
 spec_rows=[('产品类别','零食 / 干果'),('产品规格','245g / 袋'),('主要搭配','红枣 / 核桃 / 芝麻'),('包装方式','独立包装'),('食用方式','开袋即食')],
 nutrition_title='配料与营养说明', nutrition_body=['红枣、核桃与芝麻组合','具体含量以实物包装为准'],
 scene_title='一颗一袋 轻松带走', scene_subtitle='办公 / 旅途 / 茶点 / 分享', scenes=[('办公桌上','独立小袋'),('旅途补给','随手携带'),('午后茶点','搭配香茶'),('好友分享','枣核桃香')]),
product(key='date-walnut-bar', dir='date-walnut-bar-detail', name='枣仁派', eyebrow='红枣核桃果仁派', tagline='浓郁枣香 / 核桃酥香',
 product_image=ROOT/'tmp/pdfs/extracted-images/img-012.png', hero=bg_bar, process=bg_bar, scene=bg_bar,
 dark=(110,17,18), dark2=(54,6,8), accent=(228,176,75), cream=(255,241,213), ink=(94,30,24), badges=['红枣果肉','核桃仁','真材实料'],
 source_title='红枣与核桃 真材组合', source_subtitle='枣香浓郁 核桃仁香', source_statement=['红枣果肉融合核桃仁','甜香与酥香 层层交织'],
 source_features=[('优质红枣','浓郁枣香'),('核桃仁','坚果酥香'),('双料组合','口感丰富')],
 process_steps=[('红枣甄选','去核整理'),('核桃分选','核仁准备'),('压制成型','双料融合'),('包装封口','方便保存')],
 detail_title='软韧果肉 酥香核桃', detail_subtitle='切面可见 真材实料', detail_features=[('枣香浓郁','甜润软韧'),('核桃可见','颗粒酥香'),('双重口感','软韧与酥脆'),('条块成型','方便取食')],
 spec_rows=[('产品类别','零食 / 干果'),('产品规格','268g / 袋'),('主要原料','红枣 / 核桃仁'),('包装方式','袋装'),('食用方式','开袋即食')],
 nutrition_title='配料与营养说明', nutrition_body=['红枣与核桃仁组成','具体资料以实物包装为准'],
 scene_title='枣香核桃 多种时刻', scene_subtitle='茶点 / 办公 / 旅途 / 分享', scenes=[('中式茶点','搭配香茶'),('办公加餐','片刻满足'),('旅途携带','随时取食'),('亲友分享','双料枣香')]),
product(key='goji', dir='red-goji-detail', name='红枸杞', eyebrow='日常干果食材', tagline='干燥枸杞 / 多样搭配',
 product_image=ROOT/'tmp/pdfs/extracted-images/img-014.png', hero=bg_goji, process=bg_goji, scene=bg_goji,
 dark=(126,25,16), dark2=(67,10,8), accent=(230,182,75), cream=(255,246,220), ink=(104,40,22), badges=['红枸杞','袋装规格','多样吃法'],
 source_title='粒粒红润 日常好搭配', source_subtitle='甄选枸杞 干燥保存', source_statement=['红润果粒 自然干香','泡饮煮粥 均可搭配'],
 source_features=[('红润果粒','外观自然'),('干燥处理','便于保存'),('袋装规格','日常取用')],
 process_steps=[('果实采收','适时采摘'),('分选清理','去除杂质'),('干燥处理','形成干果'),('品质分选','完成封装')],
 detail_title='红润果粒 干香自然', detail_subtitle='可泡饮 可煮粥 可入汤', detail_features=[('果粒红润','自然色泽'),('干香微甜','风味柔和'),('泡饮方便','温水舒展'),('多样搭配','粥汤皆宜')],
 spec_rows=[('产品类别','零食 / 干果'),('产品规格','300g / 袋'),('产品形态','干燥枸杞'),('包装方式','袋装'),('食用方式','泡饮 / 煮粥 / 入汤')],
 nutrition_title='食用与营养说明', nutrition_body=['具体配料、营养数值与食用量','请以实物包装标注为准'],
 scene_title='一袋枸杞 多样搭配', scene_subtitle='泡水 / 煮粥 / 煲汤 / 办公', scenes=[('温水泡饮','红润舒展'),('早餐煮粥','加入谷物'),('日常煲汤','丰富搭配'),('办公泡饮','随手取用')])
]

b.OUT_ROOT = ROOT / 'output/imagegen/following-batch-5'

if __name__ == '__main__':
    b.main()
