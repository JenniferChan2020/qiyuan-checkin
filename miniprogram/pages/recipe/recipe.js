const RECIPES = [
  {
    day: '周一', emoji: '🌿', theme: '补气养血',
    breakfast: '红枣桂圆小米粥 + 水煮蛋2个 + 一小把核桃',
    lunch: '杂粮饭 + 番茄炖牛腩 + 清炒菠菜（焯水）',
    dinner: '清蒸鲈鱼 + 蒜蓉西兰花 + 紫菜蛋花汤',
    snack: '一小把蓝莓 + 黑咖啡/茶'
  },
  {
    day: '周二', emoji: '🍠', theme: '健脾抗糖',
    breakfast: '红薯 + 无糖豆浆 + 全麦吐司1片',
    lunch: '荞麦面 + 香菇滑鸡 + 凉拌紫甘蓝',
    dinner: '南瓜小米粥 + 芹菜炒香干',
    snack: '85%黑巧2小块'
  },
  {
    day: '周三', emoji: '🥩', theme: '补血重点日（猪肝）',
    breakfast: '红枣发糕 + 牛奶 + 水煮蛋',
    lunch: '米饭 + ★猪肝炒菠菜 + 凉拌木耳',
    dinner: '山药排骨汤 + 清炒莴笋',
    snack: '桑葚干一小把'
  },
  {
    day: '周四', emoji: '🐟', theme: '优质蛋白',
    breakfast: '燕麦牛奶 + 奇亚籽 + 坚果',
    lunch: '杂粮饭 + 清蒸三文鱼 + 蒜蓉芦笋',
    dinner: '鸡肉蔬菜沙拉 + 玉米半根',
    snack: '希腊酸奶 + 枸杞几粒'
  },
  {
    day: '周五', emoji: '🍲', theme: '暖身养气血',
    breakfast: '桂圆红枣茶 + 鸡蛋灌饼（少油）',
    lunch: '米饭 + 当归党参炖鸡 + 白灼菜心',
    dinner: '番茄鸡蛋荞麦面 + 一小碗芝麻糊',
    snack: '一小把黑芝麻丸'
  },
  {
    day: '周六', emoji: '🥗', theme: '抗氧化',
    breakfast: '牛油果鸡蛋全麦三明治 + 黑咖啡',
    lunch: '藜麦饭 + 牛肉沙拉 + 烤红薯',
    dinner: '豆腐蔬菜汤 + 少量糙米饭',
    snack: '混合坚果一小把'
  },
  {
    day: '周日', emoji: '🍵', theme: '轻断食·养肝血',
    breakfast: '枸杞菊花茶 + 小米南瓜粥',
    lunch: '杂粮饭 + 清炒虾仁 + 上汤娃娃菜',
    dinner: '清淡饮食：蔬菜汤 + 蒸蛋',
    snack: '红枣3颗 + 桂圆3颗'
  }
]

Page({
  data: {
    recipes: RECIPES,
    activeDay: 0
  },
  onLoad() {
    const day = new Date().getDay() // 0=周日
    const idx = day === 0 ? 6 : day - 1
    this.setData({ activeDay: idx })
  },
  switchDay(e) {
    this.setData({ activeDay: e.currentTarget.dataset.idx })
  }
})
