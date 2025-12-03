/**
 * کامپوننت نمایش نتایج پیش‌بینی
 */
export default function PredictionResult({ prediction }) {
  const formatPrice = (price) => {
    if (price >= 1000000000) {
      return (price / 1000000000).toFixed(1) + ' میلیارد تومان'
    } else if (price >= 1000000) {
      return (price / 1000000).toFixed(0) + ' میلیون تومان'
    }
    return price.toLocaleString() + ' تومان'
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-green-600'
    if (confidence >= 0.6) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getConfidenceText = (confidence) => {
    if (confidence >= 0.8) return 'عالی'
    if (confidence >= 0.6) return 'خوب'
    return 'متوسط'
  }

  return (
    <div className="card">
      <div className="text-center mb-6">
        <div className="text-4xl mb-4">🎯</div>
        <h2 className="text-2xl font-bold text-gray-800">نتایج پیش‌بینی</h2>
        <p className="text-gray-600">قیمت پیش‌بینی شده برای ملک شما</p>
      </div>

      {/* قیمت پیش‌بینی شده */}
      <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-xl p-6 mb-6 text-center">
        <p className="text-gray-600 mb-2">قیمت پیش‌بینی شده</p>
        <p className="text-4xl font-bold text-green-600">
          {formatPrice(prediction.predicted_price)}
        </p>
        <p className="text-gray-600 mt-2">
          قیمت هر متر: {formatPrice(prediction.price_per_m2)}
        </p>
      </div>

      {/* سطح اطمینان */}
      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-gray-700">سطح اطمینان پیش‌بینی:</span>
          <span className={`font-semibold ${getConfidenceColor(prediction.confidence)}`}>
            {getConfidenceText(prediction.confidence)} ({(prediction.confidence * 100).toFixed(0)}%)
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-green-500 h-2 rounded-full transition-all duration-500"
            style={{ width: `${prediction.confidence * 100}%` }}
          ></div>
        </div>
      </div>

      {/* اطلاعات ورودی */}
      <div className="border-t pt-6">
        <h3 className="font-semibold text-gray-800 mb-4">📋 اطلاعات ورودی</h3>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-600">متراژ:</span>
            <span className="font-semibold mr-2">{prediction.input_features.area} متر</span>
          </div>
          <div>
            <span className="text-gray-600">اتاق:</span>
            <span className="font-semibold mr-2">{prediction.input_features.rooms} خوابه</span>
          </div>
          <div>
            <span className="text-gray-600">سال ساخت:</span>
            <span className="font-semibold mr-2">{prediction.input_features.year_built}</span>
          </div>
          <div>
            <span className="text-gray-600">شهر:</span>
            <span className="font-semibold mr-2">{prediction.input_features.city}</span>
          </div>
          <div>
            <span className="text-gray-600">منطقه:</span>
            <span className="font-semibold mr-2">{prediction.input_features.district}</span>
          </div>
          <div>
            <span className="text-gray-600">نوع ملک:</span>
            <span className="font-semibold mr-2">
              {prediction.input_features.property_type === 'apartment' && 'آپارتمان'}
              {prediction.input_features.property_type === 'villa' && 'ویلا'}
              {prediction.input_features.property_type === 'office' && 'دفتر کار'}
              {prediction.input_features.property_type === 'store' && 'مغازه'}
              {prediction.input_features.property_type === 'land' && 'زمین'}
            </span>
          </div>
        </div>
      </div>

      {/* اطلاعات مدل */}
      <div className="border-t pt-6">
        <h3 className="font-semibold text-gray-800 mb-4">🧠 اطلاعات مدل</h3>
        <div className="bg-blue-50 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            <strong>الگوریتم:</strong> {prediction.model_info.model_type}
          </p>
          <p className="text-sm text-blue-800 mt-1">
            <strong>ویژگی‌های استفاده شده:</strong> {prediction.model_info.features_used.join('، ')}
          </p>
        </div>
      </div>

      {/* اقدامات بعدی */}
      <div className="border-t pt-6">
        <h3 className="font-semibold text-gray-800 mb-4">🚀 اقدامات بعدی</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <button className="btn-primary text-sm py-2">
            💰 محاسبه وام
          </button>
          <button className="btn-secondary text-sm py-2">
            📊 تحلیل بیشتر
          </button>
        </div>
      </div>
    </div>
  )
}