const app = getApp()

// 气血+脑疲劳专项（专为叹气/脑疲劳设计）
const ITEMS = [
  {
    id: 'breath',
    title: '腹式呼吸补气',
    icon: '🌬️',
    time: '每天5分钟',
    desc: '吸气4秒 → 屏息2秒 → 呼气6秒，用鼻子吸、嘴巴呼。激活副交感神经，直接补气、降焦虑。',
    steps: ['平躺或坐姿，一手放胸一手放腹', '吸气时让肚子鼓起（胸不动）', '呼气时肚子收回', '循环5-10分钟']
  },
  {
    id: 'taichong',
    title: '按揉太冲穴（治叹气）',
    icon: '👣',
    time: '每天2分钟',
    desc: '叹气 = 肝郁气滞。太冲穴是肝经原穴，"消气穴"。',
    steps: ['位置：脚背，大脚趾和二脚趾缝往上一横指', '用拇指按压，有酸胀感', '每脚按揉1分钟', '生气/叹气时随时按']
  },
  {
    id: 'comb',
    title: '梳头100下',
    icon: '💆',
    time: '早晚各一次',
    desc: '用木梳或牛角梳，从前额发际线梳到后颈，刺激头部经络，醒脑、助眠、养发。',
    steps: ['从前额正中梳向脑后', '左右各梳30-40下', '力度适中，头皮微热即可']
  },
  {
    id: 'pomodoro',
    title: '用脑50分钟休息10分钟',
    icon: '🧠',
    time: '工作期间',
    desc: '大脑持续高强度运转会耗气血、生虚火。强制分段，是保护脑力的关键。',
    steps: ['专注工作50分钟', '休息10分钟：离开屏幕、走动、喝水', '配合20-20-20法则：每20分钟看20英尺外20秒']
  },
  {
    id: 'sleep_23',
    title: '23点前入睡养肝血',
    icon: '🌙',
    time: '每晚',
    desc: '23点-3点是肝胆经当令，深睡才能藏血养魂。比任何补品都有效。',
    steps: ['22:30 洗漱、护肤完毕', '23:00 关灯躺下', '睡前1小时不看手机']
  },
  {
    id: 'foot',
    title: '泡脚15分钟',
    icon: '🦶',
    time: '睡前',
    desc: '引血下行，改善手脚冰凉、促进睡眠。气血不足者特别适合。',
    steps: ['水温40°C左右', '泡15-20分钟至微微出汗', '泡后按揉涌泉穴1分钟']
  }
]

Page({
  data: {
    items: [],
    doneCount: 0
  },

  onShow() {
    this.loadStatus()
  },

  loadStatus() {
    const today = app.todayStr()
    const done = app.globalData.checkInData[today] || []
    const items = ITEMS.map(i => ({ ...i, done: done.includes(i.id) }))
    this.setData({ items, doneCount: items.filter(i => i.done).length })
  },

  toggle(e) {
    const id = e.currentTarget.dataset.id
    const today = app.todayStr()
    let done = app.globalData.checkInData[today] || []
    if (done.includes(id)) done = done.filter(x => x !== id)
    else wx.vibrateShort({ type: 'light' })
    app.globalData.checkInData[today] = done
    app.saveCheckIn()
    this.loadStatus()
  },

  // 展示/隐藏步骤
  toggleSteps(e) {
    const idx = e.currentTarget.dataset.idx
    const items = this.data.items
    items[idx].expanded = !items[idx].expanded
    this.setData({ items })
  }
})
