/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `wrangler dev --local` in your terminal to start a dev server
 * - Open a new console in the sidebar to see logs
 *
 * You can take a look at the project README for more helpful tips.
 */

// R2 bucket details
const R2_BUCKET = 'emoji-puzzle'
const R2_ACCOUNT_ID = 'f64e8212f97d04229f537b65e047ae04'

// Password file name in the R2 bucket
const PASSWORD_FILE = 'passwords.json'

// Helper function to fetch a file from the R2 bucket
async function getFileFromR2(filename) {
  const r2 = new R2(`${R2_ACCOUNT_ID}.r2.cloudflarestorage.com`, {
    token: `${R2_TOKEN}`,
  })
  const file = await r2.get(`/${R2_BUCKET}/${filename}`)
  const data = await file.text()
  return JSON.parse(data)
}

// Event listener for incoming requests
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

/**
 * Fetch handler for incoming requests
 * @param {Request} request
 */
async function handleRequest(request) {
  if (request.method === 'OPTIONS') {
    return handleOptions(request)
  } else if (request.method === 'POST') {
    return handlePost(request)
  } else {
    return new Response('Method not allowed', { status: 405 })
  }
}

/**
 * Handle OPTIONS requests for CORS preflight
 * @param {Request} request
 */
function handleOptions(request) {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Max-Age': '86400',
  }
  return new Response(null, { headers })
}

/**
 * Handle POST requests to verify passwords
 * @param {Request} request
 */
async function handlePost(request) {
  const origin = request.headers.get('origin') || '*'

  const { password } = await request.json()

  // Fetch valid passwords from R2 bucket
  const validPasswords = await getFileFromR2(PASSWORD_FILE)

  // Check if the provided password matches any valid password
  const isValid = validPasswords.some(
    validPassword => validPassword.password === password.join('')
  )

  const headers = {
    'Access-Control-Allow-Origin': origin,
    'Content-Type': 'application/json',
  }

  if (isValid) {
    return new Response(JSON.stringify({ success: true }), { headers, status: 200 })
  } else {
    return new Response(JSON.stringify({ success: false }), { headers, status: 400 })
  }
}