import '@/styles/globals.css'
import Layout from '@/components/Layout'

/**
 * کامپوننت اصلی برنامه
 * این کامپوننت در تمام صفحات مشترک است
 */
export default function App({ Component, pageProps }) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  )
}