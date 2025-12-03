import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

/**
 * کامپوننت نمایش روند قیمت‌ها
 */
export default function PriceTrends({ data }) {
  // داده‌های نمونه برای روند زمانی (در نسخه واقعی از API دریافت می‌شود)
  const timeSeriesData = [
    { month: 'دی', price: 75000000, count: 45 },
    { month: 'بهمن', price: 78000000, count: 52 },
    { month: 'اسفند', price: 82000000, count: 48 },
    { month: 'فروردین', price: 85000000, count: 55 },
    { month: 'اردیبهشت', price: 88000000, count: 62 },
    { month: 'خرداد', price: 92000000, count: 58 },
  ]

  // داده‌های توزیع قیمت
  const priceDistribution = [
    { range: 'زیر ۲۰م', count: data.price_trends?.price_distribution?.under_50M || 25, color: '#10b981' },
    { range: '۲۰-۵۰م', count: data.price_trends?.price_distribution?.['50M_100M'] || 45, color: '#3b82f6' },
    { range: '۵۰-۱۰۰م', count: 35, color: '#f59e0b' },
    { range: 'بالای ۱۰۰م', count: data.price_trends?.price_distribution?.over_100M || 15, color: '#ef4444' },
  ]

  return (
    <div className="space-y-8">
      {/* روند قیمت در زمان */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-800 mb-6">📈 روند قیمت هر متر در ۶ ماه گذشته</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={timeSeriesData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis 
                tickFormatter={(value) => `${(value / 1000000).toFixed(0)}م`}
              />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'price') return [`${(value / 1000000).toFixed(0)} میلیون`, 'قیمت هر متر']
                  return [value, name]
                }}
              />
              <Legend />
              <Area 
                type="monotone" 
                dataKey="price" 
                stroke="#3b82f6" 
                fill="#3b82f6" 
                fillOpacity={0.3}
                name="قیمت هر متر (تومان)"
              />
              <Line 
                type="monotone" 
                dataKey="count" 
                stroke="#10b981" 
                name="تعداد املاک"
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* توزیع قیمت */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-800 mb-6">📊 توزیع قیمت املاک</h2>
        <div className="grid md:grid-cols-2 gap-8">
          {/* نمودار میله‌ای توزیع */}
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={priceDistribution} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="range" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#8884d8" name="تعداد املاک" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* کارت‌های خلاصه */}
          <div className="space-y-4">
            {priceDistribution.map((item, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <div 
                    className="w-4 h-4 rounded-full ml-3"
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="font-semibold text-gray-800">{item.range}</span>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-gray-800">{item.count}</p>
                  <p className="text-sm text-gray-600">ملک</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* آمار خلاصه */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="text-3xl text-blue-600 mb-3">📊</div>
          <h3 className="font-semibold text-gray-800 mb-2">میانگین قیمت هر متر</h3>
          <p className="text-2xl font-bold text-gray-800">
            {data.price_trends ? Math.round(data.price_trends.avg_price_per_m2 / 1000000) : 0} میلیون
          </p>
        </div>

        <div className="card text-center">
          <div className="text-3xl text-green-600 mb-3">📈</div>
          <h3 className="font-semibold text-gray-800 mb-2">حداکثر قیمت هر متر</h3>
          <p className="text-2xl font-bold text-gray-800">
            {data.price_trends ? Math.round(data.price_trends.price_range_per_m2?.max / 1000000) : 0} میلیون
          </p>
        </div>

        <div className="card text-center">
          <div className="text-3xl text-orange-600 mb-3">📉</div>
          <h3 className="font-semibold text-gray-800 mb-2">حداقل قیمت هر متر</h3>
          <p className="text-2xl font-bold text-gray-800">
            {data.price_trends ? Math.round(data.price_trends.price_range_per_m2?.min / 1000000) : 0} میلیون
          </p>
        </div>
      </div>
    </div>
  )
}