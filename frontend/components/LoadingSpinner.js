/**
 * کامپوننت اسپینر لودینگ
 */
export default function LoadingSpinner({ size = 'medium', text = 'در حال بارگذاری...' }) {
  const sizeClasses = {
    small: 'w-6 h-6',
    medium: 'w-12 h-12',
    large: 'w-16 h-16'
  }

  return (
    <div className="flex flex-col items-center justify-center p-8">
      <div className={`loading-spinner ${sizeClasses[size]}`}></div>
      {text && <p className="text-gray-600 mt-4">{text}</p>}
    </div>
  )
}