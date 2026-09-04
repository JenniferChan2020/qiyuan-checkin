// app.js - 元气修复·微信小程序
App({
  globalData: {
    userInfo: null,
    checkInData: {}, // { '2026-09-04': ['task1','task3'] }
   连续打卡: 0
  },

  onLaunch() {
    // 读取本地存储的打卡记录
    const saved = wx.getStorageSync('checkInData')
    if (saved) this.globalData.checkInData = saved
  },

  // 保存打卡记录
  saveCheckIn() {
    wx.setStorageSync('checkInData', this.globalData.checkInData)
  },

  // 获取今天的日期字符串
  todayStr() {
    const d = new Date()
    return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
  }
})
