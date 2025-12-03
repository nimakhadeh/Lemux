import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

/**
 * کامپوننت مقایسه شهرها
 */
export default function CityComparison({ data }) {
  const cityData = data.city_analysis || []

  // داده برای نمودار دایره‌ای
  const pieData = cityData.map(city => ({
    name: city.city,
    value: city.count,
    price: city.avg_price_per_m2
  }))

  // داده برای نمودار مقایسه قیمت
  const comparisonData = cityData.map(city => ({
    name: city.city,
    'قیمت هر متر (میلیون)': Math.round(city.avg_price_per_m2 / 1000000),
    'میانگین متراژ': Math.round(city.avg_area),
    'تعداد املاک': city.count
  }))

  // رنگ‌های نمودار دایره‌ای
  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']

  // پیدا کردن گران‌ترین و ارزان‌ترین شهر
  const mostExpensive = cityData.reduce((max, city) => 
    city.avg_price_per_m2 > max.avg_price_per_m2 ? city : max, cityData[0] || {}
  )
  
  const mostAffordable = cityData.reduce((min, city) => 
    city.avg_price_per_m2 < min.avg_price_per_m2 ? city : min, cityData[0] || {}
  )

  return (
    <div className="space-y-8">
      {/* خلاصه مقایسه */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="text-3xl text-red-500 mb-3">💰</div>
          <h3 className="font-semibold text-gray-800 mb-2">گران‌ترین شهر</h3>
          <p className="text-xl font-bold text-gray-800">{mostExpensive.city || '-'}</p>
          <p className="text-lg text-red-600">
            {mostExpensive.avg_price_per_m2 ? Math.round(mostExpensive.avg_price_per_m2 / 1000000) : 0} میلیون
          </p>
          <p className="text-sm text-gray-600">قیمت هر متر</p>
        </div>

        <div className="card text-center">
          <div className="text-3xl text-green-500 mb-3">💵</div>
          <h3 className="font-semibold text-gray-800 mb-2">مناسب‌ترین شهر</h3>
          <p className="text-xl font-bold text-gray-800">{mostAffordable.city || '-'}</p>
          <p className="text-lg text-green-600">
            {mostAffordable.avg_price_per_m2 ? Math.round(mostAffordable.avg_price_per_m2 / 1000000) : 0} میلیون
          </p>
          <p className="text-sm text-gray-600">قیمت هر متر</p>
        </div>

        <div className="card text-center">
          <div className="text-3xl text-blue-500 mb-3">🏙️</div>
          <h3 className="font-semibold text-gray-800 mb-2">تعداد شهرها</h3>
          <p className="text-3xl font-bold text-gray-800">{cityData.length}</p>
          <p className="text-sm text-gray-600">شهر تحت پوشش</p>
        </div>
      </div>

      {/* نمودار توزیع املاک */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-800 mb-6">📊 توزیع املاک در شهرها</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                outerRadius={120}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'value') return [value, 'تعداد املاک']
                  if (name === 'price') return [`${Math.round(value / 1000000)} میلیون`, 'قیمت هر متر']
                  return [value, name]
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* مقایسه قیمت و متراژ */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-800 mb-6">📈 مقایسه قیمت و متراژ در شهرها</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={comparisonData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Bar yAxisId="left" dataKey="قیمت هر متر (میلیون)" fill="#3b82f6" name="قیمت هر متر (میلیون)" />
              <Bar yAxisId="right" dataKey="میانگین متراژ" fill="#10b981" name="میانگین متراژ (متر)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* جدول مقایسه */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-800 mb-6">📋 جدول مقایسه شهرها</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="table-header">شهر</th>
                <th className="table-header">تعداد املاک</th>
                <th className="table-header">میانگین قیمت</th>
                <th className="table-header">قیمت هر متر</th>
                <th className="table-header">میانگین متراژ</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {cityData.map((city, index) => (
                <tr key={city.city} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="table-cell font-semibold">{city.city}</td>
                  <td className="table-cell">{city.count.toLocaleString()}</td>
                  <td className="table-cell">{Math.round(city.avg_price / 1000000000).toLocaleString()} میلیارد</td>
                  <td className="table-cell">{Math.round(city.avg_price_per_m2 / 1000000).toLocaleString()} میلیون</td>
                  <td className="table-cell">{Math.round(city.avg_area)} متر</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}