# Implementation Response

I'll implement the user authentication system for the Chat App according to the requirements.

## Implementation Code

### 1. User Model
File: `/src/models/user.js`

```javascript
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const SALT_WORK_FACTOR = 10;

/**
 * User Schema
 * Stores user account information with password hashing
 */
const UserSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    minlength: 3,
    maxlength: 30,
    match: /^[a-zA-Z0-9_]+$/
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true,
    match: /^\S+@\S+\.\S+$/
  },
  password: {
    type: String,
    required: true,
    minlength: 8
  },
  displayName: {
    type: String,
    required: false,
    trim: true,
    maxlength: 50
  },
  avatar: {
    type: String,
    required: false
  },
  role: {
    type: String,
    enum: ['user', 'moderator', 'admin'],
    default: 'user'
  },
  isActive: {
    type: Boolean,
    default: true
  },
  lastLogin: {
    type: Date
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
}, {
  timestamps: true
});

/**
 * Pre-save hook to hash password before saving to database
 */
UserSchema.pre('save', async function(next) {
  const user = this;
  
  // Only hash the password if it's modified or new
  if (!user.isModified('password')) return next();
  
  try {
    // Generate salt
    const salt = await bcrypt.genSalt(SALT_WORK_FACTOR);
    
    // Hash the password with the new salt
    const hashedPassword = await bcrypt.hash(user.password, salt);
    
    // Replace plaintext password with hashed one
    user.password = hashedPassword;
    next();
  } catch (error) {
    next(error);
  }
});

/**
 * Method to compare password for login
 */
UserSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

/**
 * Method to get user data without sensitive information
 */
UserSchema.methods.toPublicJSON = function() {
  return {
    id: this._id,
    username: this.username,
    email: this.email,
    displayName: this.displayName || this.username,
    avatar: this.avatar,
    role: this.role,
    createdAt: this.createdAt,
    updatedAt: this.updatedAt
  };
};

const User = mongoose.model('User', UserSchema);

module.exports = User;
```

### 2. Authentication Service
File: `/src/auth/authService.js`

```javascript
const jwt = require('jsonwebtoken');
const User = require('../models/user');
const config = require('../config');

/**
 * Authentication Service
 * Handles user authentication logic and token management
 */
class AuthService {
  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @returns {Object} Newly created user (public data only)
   */
  async registerUser(userData) {
    // Check if user already exists
    const existingUser = await User.findOne({
      $or: [
        { email: userData.email },
        { username: userData.username }
      ]
    });
    
    if (existingUser) {
      if (existingUser.email === userData.email) {
        throw new Error('Email already in use');
      } else {
        throw new Error('Username already taken');
      }
    }
    
    // Create new user
    const user = new User(userData);
    await user.save();
    
    return user.toPublicJSON();
  }
  
  /**
   * Authenticate a user and generate tokens
   * @param {string} identifier - Email or username
   * @param {string} password - User password
   * @returns {Object} Authentication data including tokens
   */
  async loginUser(identifier, password) {
    // Find user by email or username
    const user = await User.findOne({
      $or: [
        { email: identifier },
        { username: identifier }
      ]
    });
    
    if (!user) {
      throw new Error('Invalid credentials');
    }
    
    // Check if user is active
    if (!user.isActive) {
      throw new Error('Account is disabled');
    }
    
    // Validate password
    const isMatch = await user.comparePassword(password);
    if (!isMatch) {
      throw new Error('Invalid credentials');
    }
    
    // Update last login time
    user.lastLogin = new Date();
    await user.save();
    
    // Generate tokens
    const accessToken = this.generateAccessToken(user);
    const refreshToken = this.generateRefreshToken(user);
    
    return {
      user: user.toPublicJSON(),
      tokens: {
        accessToken,
        refreshToken
      }
    };
  }
  
  /**
   * Generate a short-lived access token
   * @param {Object} user - User document
   * @returns {string} JWT access token
   */
  generateAccessToken(user) {
    const payload = {
      userId: user._id,
      username: user.username,
      role: user.role
    };
    
    return jwt.sign(
      payload,
      config.auth.jwtSecret,
      { expiresIn: config.auth.accessTokenExpiry || '15m' }
    );
  }
  
  /**
   * Generate a long-lived refresh token
   * @param {Object} user - User document
   * @returns {string} JWT refresh token
   */
  generateRefreshToken(user) {
    const payload = {
      userId: user._id,
      type: 'refresh'
    };
    
    return jwt.sign(
      payload,
      config.auth.refreshTokenSecret || config.auth.jwtSecret,
      { expiresIn: config.auth.refreshTokenExpiry || '7d' }
    );
  }
  
  /**
   * Refresh an access token using a valid refresh token
   * @param {string} refreshToken - Valid refresh token
   * @returns {Object} New access token and user data
   */
  async refreshAccessToken(refreshToken) {
    if (!refreshToken) {
      throw new Error('Refresh token required');
    }
    
    try {
      // Verify refresh token
      const decoded = jwt.verify(
        refreshToken,
        config.auth.refreshTokenSecret || config.auth.jwtSecret
      );
      
      // Check token type
      if (decoded.type !== 'refresh') {
        throw new Error('Invalid token type');
      }
      
      // Find user
      const user = await User.findById(decoded.userId);
      if (!user || !user.isActive) {
        throw new Error('User not found or inactive');
      }
      
      // Generate new access token
      const accessToken = this.generateAccessToken(user);
      
      return {
        accessToken,
        user: user.toPublicJSON()
      };
    } catch (error) {
      throw new Error('Invalid or expired refresh token');
    }
  }
  
  /**
   * Verify an access token and get user data
   * @param {string} token - JWT access token
   * @returns {Object} Decoded token payload
   */
  verifyAccessToken(token) {
    if (!token) {
      throw new Error('Access token required');
    }
    
    try {
      return jwt.verify(token, config.auth.jwtSecret);
    } catch (error) {
      throw new Error('Invalid or expired access token');
    }
  }
}

module.exports = new AuthService();
```

### 3. Authentication Middleware
File: `/src/auth/authMiddleware.js`

```javascript
const authService = require('./authService');

/**
 * Authentication middleware functions
 */
const authMiddleware = {
  /**
   * Verify JWT token from Authorization header
   * Adds user payload to req.user if valid
   */
  authenticate: (req, res, next) => {
    try {
      // Get token from header
      const authHeader = req.headers.authorization;
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({
          success: false,
          message: 'Authorization token required'
        });
      }
      
      // Extract token
      const token = authHeader.split(' ')[1];
      
      // Verify token
      const payload = authService.verifyAccessToken(token);
      
      // Add user data to request
      req.user = payload;
      
      next();
    } catch (error) {
      return res.status(401).json({
        success: false,
        message: error.message || 'Authentication failed'
      });
    }
  },
  
  /**
   * Check if user has required role
   * @param {string|Array} roles - Required role(s)
   */
  authorize: (roles) => {
    return (req, res, next) => {
      // Must be used after authenticate middleware
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'User not authenticated'
        });
      }
      
      // Convert single role to array
      if (!Array.isArray(roles)) {
        roles = [roles];
      }
      
      // Check if user role is in required roles
      if (!roles.includes(req.user.role)) {
        return res.status(403).json({
          success: false,
          message: 'Access denied: Insufficient permissions'
        });
      }
      
      next();
    };
  }
};

module.exports = authMiddleware;
```

### 4. Authentication Routes
File: `/src/routes/auth.js`

```javascript
const express = require('express');
const router = express.Router();
const authService = require('../auth/authService');
const { authenticate } = require('../auth/authMiddleware');
const { validateRegistration, validateLogin } = require('../validators/authValidator');

/**
 * @route POST /api/auth/register
 * @desc Register a new user
 * @access Public
 */
router.post('/register', validateRegistration, async (req, res) => {
  try {
    const { username, email, password, displayName } = req.body;
    
    const userData = {
      username,
      email,
      password,
      displayName: displayName || username
    };
    
    const user = await authService.registerUser(userData);
    
    res.status(201).json({
      success: true,
      message: 'User registered successfully',
      data: user
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: error.message || 'Registration failed'
    });
  }
});

/**
 * @route POST /api/auth/login
 * @desc Authenticate user and get tokens
 * @access Public
 */
router.post('/login', validateLogin, async (req, res) => {
  try {
    const { identifier, password } = req.body;
    
    const authData = await authService.loginUser(identifier, password);
    
    res.status(200).json({
      success: true,
      message: 'Login successful',
      data: authData
    });
  } catch (error) {
    res.status(401).json({
      success: false,
      message: error.message || 'Authentication failed'
    });
  }
});

/**
 * @route POST /api/auth/refresh
 * @desc Refresh access token
 * @access Public (with refresh token)
 */
router.post('/refresh', async (req, res) => {
  try {
    const { refreshToken } = req.body;
    
    if (!refreshToken) {
      return res.status(400).json({
        success: false,
        message: 'Refresh token is required'
      });
    }
    
    const tokenData = await authService.refreshAccessToken(refreshToken);
    
    res.status(200).json({
      success: true,
      message: 'Token refreshed successfully',
      data: tokenData
    });
  } catch (error) {
    res.status(401).json({
      success: false,
      message: error.message || 'Token refresh failed'
    });
  }
});

/**
 * @route GET /api/auth/me
 * @desc Get current user profile
 * @access Private
 */
router.get('/me', authenticate, async (req, res) => {
  try {
    // User data is already in req.user from authenticate middleware
    // We just need to return it
    res.status(200).json({
      success: true,
      data: {
        userId: req.user.userId,
        username: req.user.username,
        role: req.user.role
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: error.message || 'Failed to retrieve user data'
    });
  }
});

module.exports = router;
```

### 5. Validation Middleware
File: `/src/validators/authValidator.js`

```javascript
const { body, validationResult } = require('express-validator');

/**
 * Middleware to validate registration input
 */
const validateRegistration = [
  body('username')
    .trim()
    .isLength({ min: 3, max: 30 })
    .withMessage('Username must be between 3 and 30 characters')
    .matches(/^[a-zA-Z0-9_]+$/)
    .withMessage('Username can only contain letters, numbers, and underscores'),
  
  body('email')
    .trim()
    .isEmail()
    .withMessage('Please provide a valid email address')
    .normalizeEmail(),
  
  body('password')
    .isLength({ min: 8 })
    .withMessage('Password must be at least 8 characters long')
    .matches(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]/)
    .withMessage('Password must contain at least one letter and one number'),
  
  body('displayName')
    .optional()
    .trim()
    .isLength({ max: 50 })
    .withMessage('Display name cannot exceed 50 characters'),
  
  // Middleware to check validation results
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }
    next();
  }
];

/**
 * Middleware to validate login input
 */
const validateLogin = [
  body('identifier')
    .trim()
    .notEmpty()
    .withMessage('Email or username is required'),
  
  body('password')
    .notEmpty()
    .withMessage('Password is required'),
  
  // Middleware to check validation results
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }
    next();
  }
];

module.exports = {
  validateRegistration,
  validateLogin
};
```

### 6. Configuration File Updates
File: `/src/config/index.js`

```javascript
// Add these configurations to your existing config file
module.exports = {
  // ... other configurations
  
  auth: {
    jwtSecret: process.env.JWT_SECRET || 'your-development-secret-key',
    refreshTokenSecret: process.env.REFRESH_TOKEN_SECRET || process.env.JWT_SECRET || 'your-refresh-secret-key',
    accessTokenExpiry: process.env.ACCESS_TOKEN_EXPIRY || '15m',
    refreshTokenExpiry: process.env.REFRESH_TOKEN_EXPIRY || '7d'
  }
};
```

### 7. API Routes Integration
File: `/src/app.js` or main Express setup file

```javascript
// Add this to your main Express app setup
const authRoutes = require('./routes/auth');

// ...

// API routes
app.use('/api/auth', authRoutes);
```

## Updated Task Status for development-state.md

### Completed
- Implemented user authentication system
  - Created User model with password hashing and validation
  - Developed JWT-based authentication service with access and refresh tokens
  - Built authentication middleware for route protection
  - Implemented registration, login, token refresh, and current user endpoints
  - Added input validation for authentication routes
  - Integrated security best practices (password hashing, JWT verification)

## Next Tasks
1. Create API endpoints for user management
   - Files: /src/routes/users.js, /src/controllers/users.js
   - Integration: Authentication system, database schema
   - Implementation: CRUD operations for user profiles

## Architecture Updates

The authentication system introduces these architecture components:

1. **Authentication Service Layer**: Handles user registration, login, and token management
2. **JWT Token Strategy**: Implements access and refresh token pattern for secure authentication
3. **Request Validation Layer**: Validates input data before processing
4. **Authorization Middleware**: Provides route protection based on authentication status and user roles

## Verification Approach

### Unit Tests
1. **User Model Tests**:
   - Test password hashing works correctly
   - Verify email/username validation rules
   - Test toPublicJSON method removes sensitive fields

2. **Auth Service Tests**:
   - Test user registration with valid/invalid data
   - Test login with correct/incorrect credentials
   - Test token generation and verification
   - Verify refresh token functionality

### API Integration Tests
1. **Registration Endpoint**: 
   - Test successful registration
   - Test duplicate username/email handling
   - Test validation error responses

2. **Login Endpoint**:
   - Test successful login
   - Test invalid credentials
   - Test disabled account handling

3. **Token Refresh Endpoint**:
   - Test valid refresh token
   - Test expired/invalid token
   - Test refresh token rotation

4. **Protected Routes**:
   - Test accessing protected routes with/without token
   - Test role-based access control

### Edge Cases to Test
- Concurrent login attempts from different devices
- Token expiration behavior
- Invalid
