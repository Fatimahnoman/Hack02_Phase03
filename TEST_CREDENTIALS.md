# Working Credentials for Authentication Testing

## New User Credentials (Just Created)
- Email: newuser@example.com
- Password: NewUserPassword123!

## Alternative Test User
- Email: testuser@example.com
- Password: TestPassword123!

## Backend Configuration
- Backend URL: http://127.0.0.1:8001
- Frontend .env.local has been updated to use this URL

## To Test Registration/Login:
1. Make sure the backend server is running on port 8001
2. Use either of the above credentials for login
3. Or register a new user with a strong password (at least 8 characters with uppercase, lowercase, and number)

## Troubleshooting:
- If you get "Login failed. Please try again.", make sure:
  1. The backend server is running on port 8001
  2. The frontend is using NEXT_PUBLIC_API_URL=http://127.0.0.1:8001
  3. You're using the correct email/password combination
  4. Your password meets requirements (uppercase, lowercase, number, special char)