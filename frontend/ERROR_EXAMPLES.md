# Error Message Examples

Visual examples of the enhanced error messages users will see on the signup page.

---

## Example 1: Username Already Taken

**Scenario**: User tries to register with an existing username

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 Username Already Taken                                       │
│                                                                  │
│ • This username is already registered in our system             │
│ • The username "john_doe" is not available                      │
│                                                                  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│ ℹ️ Suggestion: Please try a different username or sign in if    │
│   you already have an account                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 2: Password Requirements Not Met

**Scenario**: User enters a weak password

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 Password Requirements Not Met                                │
│                                                                  │
│ • Password must be at least 8 characters long                   │
│ • Password must contain at least one uppercase letter (A-Z)     │
│ • Password must contain at least one digit (0-9)                │
│                                                                  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│ ℹ️ Suggestion: Create a stronger password that includes         │
│   uppercase, lowercase, and numbers                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 3: Passwords Do Not Match

**Scenario**: User enters different passwords in the two fields

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 Passwords Do Not Match                                       │
│                                                                  │
│ • The password and confirm password fields must be identical    │
│ • Please make sure you typed the same password in both fields   │
│                                                                  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│ ℹ️ Suggestion: Check your password carefully and re-enter it    │
│   in both fields                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 4: Invalid Username Format

**Scenario**: User enters username with spaces or special characters

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 Invalid Username Format                                      │
│                                                                  │
│ • Username can only contain letters, numbers, underscores (_),  │
│   and hyphens (-)                                               │
│ • Special characters and spaces are not allowed                 │
│                                                                  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│ ℹ️ Suggestion: Try a username like: john_doe, user-123, or      │
│   myusername                                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 5: Invalid Username Length

**Scenario**: User enters a username that's too short or too long

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 Invalid Username Length                                      │
│                                                                  │
│ • Username must be between 4 and 32 characters (currently 2     │
│   characters)                                                   │
│ • Please choose a shorter or longer username                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 6: Email Already Registered

**Scenario**: User tries to register with an email that's already in use

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 Email Already Registered                                     │
│                                                                  │
│ • This email address is already associated with an account      │
│ • Each email can only be used once                              │
│                                                                  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│ ℹ️ Suggestion: Try signing in, or use a different email address │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 7: Connection Problem

**Scenario**: Network error or backend is not responding

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 Connection Problem                                           │
│                                                                  │
│ • Unable to connect to the server                               │
│ • This might be a temporary network issue                       │
│                                                                  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│ ℹ️ Suggestion: Please check your internet connection and try    │
│   again                                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 8: Server Error

**Scenario**: Backend returns HTTP 500 error

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 Server Error                                                 │
│                                                                  │
│ • The server encountered an unexpected error                    │
│ • This is not your fault - something went wrong on our end      │
│                                                                  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│ ℹ️ Suggestion: Please try again in a few moments, or contact    │
│   support if the problem persists                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 9: Database Error

**Scenario**: Database connection or operation fails

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 Database Error                                               │
│                                                                  │
│ • There was a problem saving your account                       │
│ • The database service may be temporarily unavailable           │
│                                                                  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│ ℹ️ Suggestion: Please try again in a moment                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 10: Service Unavailable

**Scenario**: Backend returns HTTP 503 status

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 Service Unavailable                                          │
│                                                                  │
│ • The server is temporarily unavailable                         │
│                                                                  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│ ℹ️ Suggestion: Please try again in a few minutes                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 11: Multiple Password Issues

**Scenario**: Password missing multiple requirements

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 Password Requirements Not Met                                │
│                                                                  │
│ • Password must contain at least one uppercase letter (A-Z)     │
│ • Password must contain at least one lowercase letter (a-z)     │
│ • Password must contain at least one digit (0-9)                │
│ • Password must be at least 8 characters long                   │
│                                                                  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│ ℹ️ Suggestion: Create a stronger password that includes         │
│   uppercase, lowercase, and numbers                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Visual Design Elements

### Color Scheme
- **Background**: Light red (`bg-red-50`)
- **Border**: Dark red, 2px (`border-red-200`, `border-2`)
- **Title**: Dark red, bold (`text-red-900`, `font-bold`)
- **Details**: Red text (`text-red-800`)
- **Bullets**: Red circles (`text-red-600`)
- **Suggestion**: Red with bold label (`text-red-700`)

### Icons
- **Error Icon**: ❌ (red X circle, 24x24px)
- **Info Icon**: ℹ️ (info circle, 20x20px)

### Spacing
- **Padding**: 20px all around
- **Title margin**: 8px bottom
- **Detail spacing**: 6px between items
- **Suggestion divider**: 12px top margin, 12px top padding

### Typography
- **Title**: 16px, bold, red-900
- **Details**: 14px, regular, red-800
- **Suggestion**: 14px, medium weight, red-700
- **Suggestion label**: Bold

---

## Comparison: Before vs After

### Before (Generic Error)
```
┌─────────────────────────────────────────────────────────────────┐
│ ❌ Registration failed. Please try again.                       │
└─────────────────────────────────────────────────────────────────┘
```

### After (Detailed Error)
```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 Username Already Taken                                       │
│                                                                  │
│ • This username is already registered in our system             │
│ • The username "john_doe" is not available                      │
│                                                                  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│ ℹ️ Suggestion: Please try a different username or sign in if    │
│   you already have an account                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Improvement**: 
- ✅ Clear error category
- ✅ Specific details about the problem
- ✅ Actionable suggestion
- ✅ Professional appearance

---

## Testing the Errors

To see these errors in action:

1. **Username exists**: 
   - Create account with "testuser"
   - Try to create another with "testuser"

2. **Weak password**: 
   - Enter password: "abc"
   - Submit form

3. **Password mismatch**: 
   - Password: "TestPass123"
   - Confirm: "Different456"

4. **Invalid username**: 
   - Username: "test user@123"
   - Submit form

5. **Network error**: 
   - Stop backend server
   - Try to register

Each will show a different, specific error message! 🎯

