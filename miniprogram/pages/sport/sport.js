const SPORTS = [
  {
    day: '周一', emoji: '🏃', type: '有氧', duration: '30分钟',
    desc: '快走/慢跑/跳绳/跟练HIIT视频',
    warmup: ['开合跳 30秒', '原地高抬腿 30秒', '手臂环绕 10次'],
    main: ['★ 快走或慢跑 20分钟（能说话但不能唱歌的强度）', '★ 跳绳 3组×100个', '★ 波比跳 3组×10次'],
    stretch: ['大腿前侧拉伸 30秒×2', '臀部拉伸 30秒×2', '猫牛式 10次']
  },
  {
    day: '周二', emoji: '💪', type: '力量·上肢核心', duration: '30分钟',
    desc: '在家无器械也能练',
    warmup: ['原地小跑 1分钟', '肩关节环绕 10次'],
    main: ['★ 俯卧撑 3组×12次（跪姿也可）', '★ 平板支撑 3组×30-45秒', '★ 卷腹 3组×15次', '★ 俄罗斯转体 3组×20次'],
    stretch: ['胸肌拉伸 30秒×2', '腹部拉伸（眼镜蛇式）30秒']
  },
  {
    day: '周三', emoji: '🧘', type: '休息·恢复', duration: '轻活动',
    desc: '休息日≠躺平，散步+拉伸',
    warmup: ['无'],
    main: ['饭后散步 20分钟', '全身拉伸 10分钟', '泡沫轴放松肌肉'],
    stretch: ['下犬式 30秒', '鸽子式 每侧30秒', '婴儿式 1分钟']
  },
  {
    day: '周四', emoji: '🦵', type: '力量·下肢臀', duration: '30分钟',
    desc: '练腿臀，提升代谢',
    warmup: ['原地踏步 1分钟', '髋关节环绕 10次'],
    main: ['★ 深蹲 3组×15次', '★ 弓步蹲 每侧3组×12次', '★ 臀桥 3组×20次', '★ 侧抬腿 每侧3组×15次'],
    stretch: ['股四头肌拉伸 30秒×2', '臀部拉伸 30秒×2', '小腿拉伸 30秒×2']
  },
  {
    day: '周五', emoji: '⚡', type: 'HIIT', duration: '25分钟',
    desc: '高强度间歇，燃脂效率高',
    warmup: ['开合跳 1分钟', '原地高抬腿 30秒'],
    main: ['★ 每个动作45秒+休息15秒，循环3轮：', '　深蹲跳 / 俯卧撑 / 登山跑 / 波比跳 / 高抬腿'],
    stretch: ['全身拉伸 5分钟']
  },
  {
    day: '周六', emoji: '🧘', type: '瑜伽·柔韧', duration: '30分钟',
    desc: '放松身心，缓解脑疲劳',
    warmup: ['婴儿式 1分钟'],
    main: ['★ 拜日式 A 5遍', '★ 战士一式/二式 每侧30秒', '★ 三角式 每侧30秒', '★ 坐姿前屈 1分钟'],
    stretch: ['摊尸式（Savasana）3分钟']
  },
  {
    day: '周日', emoji: '🌿', type: '休息', duration: '轻活动',
    desc: '完全休息，为下周蓄能',
    warmup: ['无'],
    main: ['饭后散步 20分钟', '深呼吸练习 5分钟', '按揉太冲穴（疏肝）'],
    stretch: ['睡前全身拉伸 10分钟']
  }
]

Page({
  data: {
    sports: SPORTS,
    activeDay: 0
  },
  onLoad() {
    const day = new Date().getDay()
    const idx = day === 0 ? 6 : day - 1
    this.setData({ activeDay: idx })
  },
  switchDay(e) {
    this.setData({ activeDay: e.currentTarget.dataset.idx })
  }
})
