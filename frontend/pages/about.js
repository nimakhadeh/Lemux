import Head from 'next/head'
import Layout from '@/components/Layout'

/**
 * صفحه درباره ما
 */
export default function About() {
  return (
    <>
      <Head>
        <title>درباره ما - PropAnalyzer</title>
        <meta name="description" content="درباره پروژه PropAnalyzer و تیم توسعه" />
      </Head>

      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            {/* هدر صفحه */}
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold text-gray-800 mb-4">درباره PropAnalyzer</h1>
              <p className="text-xl text-gray-600">
                پلتفرم هوشمند تحلیل بازار مسکن ایران
              </p>
            </div>

            {/* محتوای اصلی */}
            <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">🎯 هدف ما</h2>
              <p className="text-gray-700 leading-relaxed mb-6">
                PropAnalyzer با هدف ایجاد شفافیت در بازار مسکن ایران و کمک به سرمایه‌گذاران، 
                خریداران و فروشندگان برای تصمیم‌گیری‌های بهتر ایجاد شده است. ما با استفاده از 
                هوش مصنوعی و تحلیل داده‌های واقعی، اطلاعات دقیق و قابل اعتمادی را در اختیار 
                کاربران قرار می‌دهیم.
              </p>

              <div className="grid md:grid-cols-2 gap-8 mb-8">
                <div className="card">
                  <h3 className="text-lg font-semibold mb-3">📊 تحلیل داده‌محور</h3>
                  <p className="text-gray-600">
                    جمع‌آوری و تحلیل هزاران داده واقعی از بازار برای ارائه دقیق‌ترین تحلیلها
                  </p>
                </div>

                <div className="card">
                  <h3 className="text-lg font-semibold mb-3">🤖 هوش مصنوعی</h3>
                  <p className="text-gray-600">
                    استفاده از پیشرفته‌ترین الگوریتم‌های ML برای پیش‌بینی قیمت و روند بازار
                  </p>
                </div>

                <div className="card">
                  <h3 className="text-lg font-semibold mb-3">🌐 پوشش ملی</h3>
                  <p className="text-gray-600">
                    پوشش کامل شهرهای بزرگ ایران و تحلیل بازار در سطح منطقه‌ای
                  </p>
                </div>

                <div className="card">
                  <h3 className="text-lg font-semibold mb-3">⚡ بروزرسانی لحظه‌ای</h3>
                  <p className="text-gray-600">
                    بروزرسانی مداوم داده‌ها و آنالیزها برای ارائه اطلاعات به‌روز
                  </p>
                </div>
              </div>
            </div>

            {/* ویژگی‌های فنی */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">🛠️ فناوری‌های به کار رفته</h2>
              
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-3xl mb-3">🐍</div>
                  <h4 className="font-semibold mb-2">Backend</h4>
                  <p className="text-sm text-gray-600">Django REST Framework + PostgreSQL</p>
                </div>

                <div className="text-center">
                  <div className="text-3xl mb-3">⚡</div>
                  <h4 className="font-semibold mb-2">AI Service</h4>
                  <p className="text-sm text-gray-600">FastAPI + Scikit-learn</p>
                </div>

                <div className="text-center">
                  <div className="text-3xl mb-3">🕷️</div>
                  <h4 className="font-semibold mb-2">Data Collection</h4>
                  <p className="text-sm text-gray-600">Scrapy Crawlers</p>
                </div>

                <div className="text-center">
                  <div className="text-3xl mb-3">⚛️</div>
                  <h4 className="font-semibold mb-2">Frontend</h4>
                  <p className="text-sm text-gray-600">Next.js + Tailwind CSS</p>
                </div>

                <div className="text-center">
                  <div className="text-3xl mb-3">🐳</div>
                  <h4 className="font-semibold mb-2">Deployment</h4>
                  <p className="text-sm text-gray-600">Docker + Docker Compose</p>
                </div>

                <div className="text-center">
                  <div className="text-3xl mb-3">📈</div>
                  <h4 className="font-semibold mb-2">Analytics</h4>
                  <p className="text-sm text-gray-600">Recharts + Custom Dashboards</p>
                </div>
              </div>
            </div>

            {/* CTA */}
            <div className="text-center mt-12">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">
                آماده شروع تحلیل هستید؟
              </h3>
              <div className="flex flex-wrap justify-center gap-4">
                <a href="/" className="btn-primary">
                  🏠 مشاهده املاک
                </a>
                <a href="/dashboard" className="btn-secondary">
                  📊 رفتن به داشبورد
                </a>
                <a href="/predict" className="btn-primary bg-green-600 hover:bg-green-700">
                  🤖 پیش‌بینی قیمت
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}