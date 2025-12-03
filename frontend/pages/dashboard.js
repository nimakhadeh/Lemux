import { useState, useEffect } from 'react'
import Head from 'next/head'
import axios from 'axios'
import MarketAnalysis from '@/components/MarketAnalysis'
import PriceTrends from '@/components/PriceTrends'
import CityComparison from '@/components/CityComparison'
import LoadingSpinner from '@/components/LoadingSpinner'

/**
 * صفحه داشبورد تحلیل - نمایش آمار و نمودارهای پیشرفته
 */
export default function Dashboard() {
  const [analysisData, setAnalysisData] = useState(null)
  const [marketData, setMarketData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    fetchAnalysisData()
    fetchMarketData()
  }, [])

  // دریافت داده‌های تحلیل از AI API
  const fetchAnalysisData = async () => {
    try {
      const response = await axios.get('http://localhost:8001/analyze/')
      setAnalysisData(response.data)
    } catch (err) {
      console.error('Error fetching analysis data:', err)
      setError('خطا در دریافت داده‌های تحلیل')
      // داده‌های نمونه
      setAnalysisData(sampleAnalysisData)
    }
  }

  // دریافت داده‌های بازار از Django API
  const fetchMarketData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/listings/stats/')
      setMarketData(response.data)
    } catch (err) {
      console.error('Error fetching market data:', err)
      // داده‌های نمونه
      setMarketData(sampleMarketData)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>داشبورد تحلیل - PropAnalyzer</title>
        <meta name="description" content="داشبورد پیشرفته تحلیل بازار مسکن" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* هدر داشبورد */}
        <div className="bg-white shadow-sm border-b">
          <div className="container mx-auto px-4 py-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h1 className="text-2xl font-bold text-gray-800">📊 داشبورد تحلیل بازار</h1>
                <p className="text-gray-600 mt-1">تحلیل جامع و آنلاین بازار مسکن ایران</p>
              </div>
              
              <div className="flex flex-wrap gap-2">
                <button 
                  onClick={() => setActiveTab('overview')}
                  className={`px-4 py-2 rounded-lg transition ${
                    activeTab === 'overview' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  📈 نمای کلی
                </button>
                <button 
                  onClick={() => setActiveTab('cities')}
                  className={`px-4 py-2 rounded-lg transition ${
                    activeTab === 'cities' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  🏙️ تحلیل شهرها
                </button>
                <button 
                  onClick={() => setActiveTab('trends')}
                  className={`px-4 py-2 rounded-lg transition ${
                    activeTab === 'trends' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  📊 روندها
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* محتوای اصلی */}
        <div className="container mx-auto px-4 py-8">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <div className="flex items-center">
                <div className="text-red-500 text-lg">⚠️</div>
                <div className="mr-3">
                  <h4 className="text-red-800 font-semibold">خطا در دریافت داده</h4>
                  <p className="text-red-600 text-sm">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* تب نمای کلی */}
          {activeTab === 'overview' && analysisData && (
            <div className="space-y-6">
              {/* کارت‌های آمار سریع */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="card text-center">
                  <div className="text-2xl mb-2">🏠</div>
                  <h3 className="text-lg font-semibold text-gray-800">تعداد املاک</h3>
                  <p className="text-2xl font-bold text-blue-600">
                    {marketData?.overall?.total_listings?.toLocaleString() || '0'}
                  </p>
                </div>

                <div className="card text-center">
                  <div className="text-2xl mb-2">💰</div>
                  <h3 className="text-lg font-semibold text-gray-800">میانگین قیمت</h3>
                  <p className="text-2xl font-bold text-green-600">
                    {(marketData?.overall?.avg_price / 1000000)?.toFixed(0) || '0'} میلیون
                  </p>
                </div>

                <div className="card text-center">
                  <div className="text-2xl mb-2">📐</div>
                  <h3 className="text-lg font-semibold text-gray-800">میانگین متراژ</h3>
                  <p className="text-2xl font-bold text-purple-600">
                    {marketData?.overall?.avg_area?.toFixed(0) || '0'} متر
                  </p>
                </div>

                <div className="card text-center">
                  <div className="text-2xl mb-2">🏙️</div>
                  <h3 className="text-lg font-semibold text-gray-800">شهرهای تحت پوشش</h3>
                  <p className="text-2xl font-bold text-orange-600">
                    {analysisData?.city_analysis?.length || '0'}
                  </p>
                </div>
              </div>

              {/* تحلیل بازار */}
              {analysisData && <MarketAnalysis data={analysisData} />}

              {/* توصیه‌ها */}
              {analysisData?.recommendations && (
                <div className="card">
                  <h2 className="text-xl font-bold text-gray-800 mb-4">💡 توصیه‌های سرمایه‌گذاری</h2>
                  <div className="space-y-3">
                    {analysisData.recommendations.map((recommendation, index) => (
                      <div key={index} className="flex items-start p-3 bg-blue-50 rounded-lg">
                        <div className="text-blue-500 mt-1 ml-3">•</div>
                        <p className="text-gray-700">{recommendation}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* تب تحلیل شهرها */}
          {activeTab === 'cities' && analysisData && (
            <CityComparison data={analysisData} />
          )}

          {/* تب روندها */}
          {activeTab === 'trends' && analysisData && (
            <PriceTrends data={analysisData} />
          )}
        </div>
      </div>
    </>
  )
}

// داده‌های نمونه برای توسعه
const sampleAnalysisData = {
  overall_stats: {
    total_listings: 150,
    avg_price: 12500000000,
    avg_price_per_m2: 85000000,
    avg_area: 95,
    avg_rooms: 2.5
  },
  city_analysis: [
    {
      city: 'تهران',
      count: 85,
      avg_price: 14500000000,
      avg_price_per_m2: 95000000,
      avg_area: 92
    },
    {
      city: 'مشهد',
      count: 25,
      avg_price: 8500000000,
      avg_price_per_m2: 65000000,
      avg_area: 98
    },
    {
      city: 'اصفهان',
      count: 20,
      avg_price: 7500000000,
      avg_price_per_m2: 55000000,
      avg_area: 105
    },
    {
      city: 'شیراز',
      count: 15,
      avg_price: 6800000000,
      avg_price_per_m2: 48000000,
      avg_area: 110
    }
  ],
  property_type_analysis: [
    {
      property_type: 'apartment',
      count: 120,
      avg_price: 11500000000,
      avg_price_per_m2: 82000000
    },
    {
      property_type: 'villa',
      count: 20,
      avg_price: 28500000000,
      avg_price_per_m2: 120000000
    },
    {
      property_type: 'store',
      count: 10,
      avg_price: 8500000000,
      avg_price_per_m2: 95000000
    }
  ],
  price_trends: {
    avg_price_per_m2: 85000000,
    price_range_per_m2: {
      min: 35000000,
      max: 185000000
    },
    price_distribution: {
      under_50M: 45,
      50M_100M: 75,
      over_100M: 30
    }
  },
  recommendations: [
    'بالاترین قیمت هر متر در تهران است',
    'مناسب‌ترین قیمت هر متر در شیراز مشاهده می‌شود',
    'بازار در وضعیت متعادل قرار دارد',
    'حجم داده‌های بازار مناسب است - تحلیل قابل اعتماد'
  ]
}

const sampleMarketData = {
  overall: {
    total_listings: 150,
    avg_price: 12500000000,
    avg_price_per_m2: 85000000,
    avg_area: 95,
    avg_rooms: 2.5
  },
  by_city: [
    { city: 'تهران', count: 85 },
    { city: 'مشهد', count: 25 },
    { city: 'اصفهان', count: 20 },
    { city: 'شیراز', count: 15 }
  ]
}