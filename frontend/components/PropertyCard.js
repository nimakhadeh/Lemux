import Link from 'next/link'

/**
 * کامپوننت کارت نمایش ملک
 */
export default function PropertyCard({ property }) {
  const formatPrice = (price) => {
    if (price >= 1000000000) {
      return (price / 1000000000).toFixed(1) + ' میلیارد'
    } else if (price >= 1000000) {
      return (price / 1000000).toFixed(0) + ' میلیون'
    }
    return price.toLocaleString()
  }

  const getPropertyTypeIcon = (type) => {
    switch (type) {
      case 'apartment': return '🏢'
      case 'villa': return '🏡'
      case 'office': return '🏢'
      case 'store': return '🏪'
      case 'land': return '🏞️'
      default: return '🏠'
    }
  }

  const getConditionBadge = (condition) => {
    const badges = {
      new: { text: 'نوساز', color: 'bg-green-100 text-green-800' },
      renovated: { text: 'بازسازی', color: 'bg-blue-100 text-blue-800' },
      normal: { text: 'معمولی', color: 'bg-gray-100 text-gray-800' },
      old: { text: 'قدیمی', color: 'bg-orange-100 text-orange-800' }
    }
    
    const badge = badges[condition] || badges.normal
    return (
      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${badge.color}`}>
        {badge.text}
      </span>
    )
  }

  return (
    <div className="card group hover:shadow-lg transition duration-300">
      <Link href={`/listings/${property.id}`}>
        <div className="cursor-pointer">
          {/* هدر کارت */}
          <div className="flex justify-between items-start mb-3">
            <div className="flex items-center space-x-2 space-x-reverse">
              <span className="text-2xl">{getPropertyTypeIcon(property.property_type)}</span>
              <div>
                {getConditionBadge(property.condition)}
              </div>
            </div>
            <div className="text-left">
              <p className="text-2xl font-bold text-green-600">
                {formatPrice(property.price)}
              </p>
              {property.area && (
                <p className="text-sm text-gray-500">
                  {(property.price / property.area).toLocaleString()} تومان/متر
                </p>
              )}
            </div>
          </div>

          {/* عنوان و آدرس */}
          <h3 className="font-semibold text-gray-800 mb-2 line-clamp-2 group-hover:text-blue-600 transition">
            {property.title}
          </h3>
          
          <p className="text-gray-600 text-sm mb-4 line-clamp-2 flex items-start">
            <span className="ml-1 mt-1 flex-shrink-0">📍</span>
            <span>{property.address}</span>
          </p>

          {/* مشخصات فنی */}
          <div className="grid grid-cols-3 gap-2 py-3 border-t border-gray-100">
            <div className="text-center">
              <div className="text-gray-500 text-sm">متراژ</div>
              <div className="font-semibold text-gray-800">{property.area} متر</div>
            </div>
            <div className="text-center">
              <div className="text-gray-500 text-sm">اتاق</div>
              <div className="font-semibold text-gray-800">{property.rooms} خوابه</div>
            </div>
            <div className="text-center">
              <div className="text-gray-500 text-sm">ساخت</div>
              <div className="font-semibold text-gray-800">{property.year_built}</div>
            </div>
          </div>

          {/* فوتر کارت */}
          <div className="flex justify-between items-center pt-3 border-t border-gray-100">
            <div className="text-sm text-gray-500">
              {property.city} - {property.district}
            </div>
            <div className="text-blue-600 text-sm font-semibold group-hover:text-blue-700 transition">
              مشاهده جزئیات →
            </div>
          </div>
        </div>
      </Link>
    </div>
  )
}