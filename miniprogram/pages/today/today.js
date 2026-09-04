const app = getApp()

// 每日打卡任务定义（针对：熬夜/嗜甜/缺运动/气血不足/叹气/脑疲劳）
const TASKS = [
  { id: 'no_sugar',   icon: '🚫', title: '没喝奶茶/甜饮料', cat: '抗糖' },
  { id: 'veggie',     icon: '🥬', title: '吃了深色蔬菜', cat: '抗糖' },
  { id: 'whole_grain',icon: '🌾', title: '主食换了一半杂粮', cat: '抗糖' },
  { id: 'sleep_23',   icon: '🌙', title: '23点前护肤躺下', cat: '作息' },
  { id: 'wake_fixed', icon: '☀️', title: '固定时间起床', cat: '作息' },
  { id: 'sport',      icon: '🏃', title: '运动30分钟', cat: '运动' },
  { id: 'breath',     icon: '🌬️', title: '腹式呼吸5分钟（补气）', cat: '气血' },
  { id: 'taichong',   icon: '👣', title: '按揉太冲穴2分钟（治叹气）', cat: '气血' },
  { id: 'pomodoro',   icon: '🧠', title: '用脑50分钟休息10分钟', cat: '健脑' },
  { id: 'comb',       icon: '💆', title: '梳头100下（醒脑）', cat: '健脑' },
  { id: 'skincare_am',icon: '🧴', title: '早：维C+防晒', cat: '护肤' },
  { id: 'skincare_pm',icon: '🌸', title: '晚：维A酸（隔天）', cat: '护肤' }
]

const CATEGORIES = [
  { key: '抗糖', name: '抗糖饮食', emoji: '🍯' },
  { key: '作息', name: '作息节律', emoji: '🌙' },
  { key: '运动', name: '运动', emoji: '🏃' },
  { key: '气血', name: '气血专项', emoji: '🌬️' },
  { key: '健脑', name: '健脑', emoji: '🧠' },
  { key: '护肤', name: '护肤', emoji: '🧴' }
]

Page({
  data: {
    categories: CATEGORIES,
    today: '',
    tasks: [],
    doneCount: 0,
    streak: 0,
    progressPercent: 0,
    motto: ''
  },

  onLoad() {
    this.setData({ today: app.todayStr() })
    this.loadTasks()
    this.setMotto()
  },

  onShow() {
    // 返回时刷新
    if (this.data.today !== app.todayStr()) {
      this.setData({ today: app.todayStr() })
    }
    this.loadTasks()
    this.calcStreak()
  },

  // 加载今日打卡状态
  loadTasks() {
    const done = app.globalData.checkInData[this.data.today] || []
    const tasks = TASKS.map(t => ({ ...t, done: done.includes(t.id) }))
    const doneCount = done.length
    this.setData({
      tasks,
      doneCount,
      progressPercent: Math.round(doneCount / TASKS.length * 100)
    })
  },

  // 切换打卡状态
  toggleTask(e) {
    const id = e.currentTarget.dataset.id
    const today = this.data.today
    let done = app.globalData.checkInData[today] || []
    if (done.includes(id)) {
      done = done.filter(x => x !== id)
    } else {
      done.push(id)
      wx.vibrateShort({ type: 'light' }) // 震动反馈
    }
    app.globalData.checkInData[today] = done
    app.saveCheckIn()
    this.loadTasks()
    this.calcStreak()
  },

  // 计算连续打卡天数
  calcStreak() {
    let streak = 0
    const data = app.globalData.checkInData
    const now = new Date()
    for (let i = 0; i < 365; i++) {
      const d = new Date(now.getTime() - i * 86400000)
      const key = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
      if (data[key] && data[key].length > 0) streak++
      else if (i > 0) break // 今天没打卡不算断
    }
    this.setData({ streak })
  },

  // 每日一句
  setMotto() {
    const mottos = [
      '36岁，是开始好好爱自己的年纪 🌿',
      '皮肤28天换一轮，坚持就有光 ✨',
      '叹气是肝气在求救，深呼吸把它抚平 🌬️',
      '你不需要完美，只需要每天都比昨天好一点 🌸',
      '气血足了，人自然就亮了 🕯️',
      '早睡是最好的医美，运动是最便宜的抗衰药 💪',
      '别急，身体会奖励每一个认真对待它的人 🎁'
    ]
    const idx = new Date().getDate() % mottos.length
    this.setData({ motto: mottos[idx] })
  }
})
