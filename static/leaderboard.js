// models/User.js - Add these fields to User schema
const UserSchema = new mongoose.Schema({
    // ... existing fields ...
    points: {
      type: Number,
      default: 0
    },
    badges: [String],
    contributions: {
      posts: { type: Number, default: 0 },
      comments: { type: Number, default: 0 },
      upvotesReceived: { type: Number, default: 0 }
    },
    rank: {
      type: String,
      enum: ['novice', 'contributor', 'expert', 'master'],
      default: 'novice'
    }
  });
  
  // routes/leaderboard.js
  router.get('/', async (req, res) => {
    try {
      const users = await User.find().sort({ points: -1 }).limit(50);
      res.json(users);
    } catch (err) {
      console.error(err.message);
      res.status(500).send('Server error');
    }
  });