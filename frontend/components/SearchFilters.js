import { useState } from 'react'

/**
 * کامپوننت فیلترهای جستجو
 */
export default function SearchFilters({ onFilter }) {
  const [filters, setFilters] = useState({
    city: '',
    minPrice: '',
    maxPrice: '',
    propertyType: '',
    rooms: ''
  })

  const cities = ['تهران', 'مشهد', 'اصفهان', 'شیراز', 'تبریز', 'کرج']
  const propertyTypes = [
    { value: 'apartment', label: 'آپارتمان' },
    { value: 'villa', label: 'ویلا' },
    { value: 'office', label: 'دفتر کار' },
    { value: 'store', label: 'مغازه' },
    { value: 'land', label: 'زمین' }
  ]
  const roomOptions = ['1', '2', '3', '4', '5+']

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value }
    setFilters(newFilters)
    onFilter(newFilters)
  }

  const clearFilters = () => {
    const emptyFilters = {
      city: '',
      minPrice: '',
      maxPrice: '',
      propertyType: '',
      rooms: ''
    }
    setFilters(emptyFilters)
    onFilter(emptyFilters)
  }

  return (
    <div className="card">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4 sm:mb-0">🔍 فیلترهای جستجو</h2>
        <button
          onClick={clearFilters}
          className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:border-gray-400 transition"
        >
          پاک کردن فیلترها
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* شهر */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🏙️ شهر
          </label>
          <select
            value={filters.city}
            onChange={(e) => handleFilterChange('city', e.target.value)}
            className="input-field"
          >
            <option value="">همه شهرها</option>
            {cities.map(city => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>
        </div>

        {/* نوع ملک */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🏠 نوع ملک
          </label>
          <select
            value={filters.propertyType}
            onChange={(e) => handleFilterChange('propertyType', e.target.value)}
            className="input-field"
          >
            <option value="">همه انواع</option>
            {propertyTypes.map(type => (
              <option key={type.value} value={type.value}>{type.label}</option>
            ))}
          </select>
        </div>

        {/* تعداد اتاق */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🚪 تعداد اتاق
          </label>
          <select
            value={filters.rooms}
            onChange={(e) => handleFilterChange('rooms', e.target.value)}
            className="input-field"
          >
            <option value="">همه</option>
            {roomOptions.map(rooms => (
              <option key={rooms} value={rooms}>{rooms} خوابه</option>
            ))}
          </select>
        </div>

        {/* حداقل قیمت */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            💰 حداقل قیمت
          </label>
          <select
            value={filters.minPrice}
            onChange={(e) => handleFilterChange('minPrice', e.target.value)}
            className="input-field"
          >
            <option value="">هر قیمتی</option>
            <option value="1000000000">۱ میلیارد</option>
            <option value="5000000000">۵ میلیارد</option>
            <option value="10000000000">۱۰ میلیارد</option>
            <option value="20000000000">۲۰ میلیارد</option>
          </select>
        </div>

        {/* حداکثر قیمت */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            💵 حداکثر قیمت
          </label>
          <select
            value={filters.maxPrice}
            onChange={(e) => handleFilterChange('maxPrice', e.target.value)}
            className="input-field"
          >
            <option value="">هر قیمتی</option>
            <option value="5000000000">۵ میلیارد</option>
            <option value="10000000000">۱۰ میلیارد</option>
            <option value="20000000000">۲۰ میلیارد</option>
            <option value="50000000000">۵۰ میلیارد</option>
          </select>
        </div>
      </div>

      {/* نمایش فیلترهای فعال */}
      <div className="mt-4 flex flex-wrap gap-2">
        {filters.city && (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
            شهر: {filters.city}
            <button
              onClick={() => handleFilterChange('city', '')}
              className="mr-1 hover:text-blue-600"
            >
              ×
            </button>
          </span>
        )}
        {filters.propertyType && (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs bg-green-100 text-green-800">
            نوع: {propertyTypes.find(t => t.value === filters.propertyType)?.label}
            <button
              onClick={() => handleFilterChange('propertyType', '')}
              className="mr-1 hover:text-green-600"
            >
              ×
            </button>
          </span>
        )}
        {filters.rooms && (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs bg-purple-100 text-purple-800">
            اتاق: {filters.rooms} خوابه
            <button
              onClick={() => handleFilterChange('rooms', '')}
              className="mr-1 hover:text-purple-600"
            >
              ×
            </button>
          </span>
        )}
        {(filters.minPrice || filters.maxPrice) && (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs bg-orange-100 text-orange-800">
            قیمت: {filters.minPrice ? `${(filters.minPrice / 1000000000).toFixed(0)}م` : ''} 
            {filters.minPrice && filters.maxPrice ? ' - ' : ''}
            {filters.maxPrice ? `${(filters.maxPrice / 1000000000).toFixed(0)}م` : ''}
            <button
              onClick={() => {
                handleFilterChange('minPrice', '')
                handleFilterChange('maxPrice', '')
              }}
              className="mr-1 hover:text-orange-600"
            >
              ×
            </button>
          </span>
        )}
      </div>
    </div>
  )
}