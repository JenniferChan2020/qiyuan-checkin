const app = getApp()

Page({
  data: {
    streak: 0,
    totalDays: 0,
    totalChecks: 0,
    avgRate: 0,
    chartData: [], // 近7天 {day, count, percent, max}
    todayCount: 0,
    todayTotal: 12
  },

  onShow() {
    this.calcAll()
  },

  calcAll() {
    const data = app.globalData.checkInData
    const days = Object.keys(data)

    // 连续打卡
    let streak = 0
    const now = new Date()
    for (let i = 0; i < 365; i++) {
      const d = new Date(now.getTime() - i * 86400000)
      const key = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
      if (data[key] && data[key].length > 0) streak++
      else if (i > 0) break
    }

    // 总打卡次数
    let totalChecks = 0
    days.forEach(k => totalChecks += data[k].length)

    // 近7天图表数据
    const chartData = []
    for (let i = 6; i >= 0; i--) {
      const d = new Date(now.getTime() - i * 86400000)
      const key = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
      const count = (data[key] || []).length
      chartData.push({
        day: `${d.getMonth()+1}/${d.getDate()}`,
        count,
        percent: Math.round(count / 12 * 100),
        max: 12
      })
    }

    const today = app.todayStr()
    const todayCount = (data[today] || []).length

    this.setData({
      streak,
      totalDays: days.length,
      totalChecks,
      avgRate: days.length ? Math.round(totalChecks / (days.length * 12) * 100) : 0,
      chartData,
      todayCount
    })
  },

  // 清空数据（调试用）
  clearData() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有打卡记录吗？此操作不可恢复。',
      success(res) {
        if (res.confirm) {
          app.globalData.checkInData = {}
          app.saveCheckIn()
          this.calcAll()
        }
      }
    })
  }
})
