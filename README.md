# Customer Support System

A professional AI-powered customer support system a company specializing in custom sign design and production. This system provides a conversational interface to gather customer requirements and create accurate design mockups.

## Features

### 🎨 Professional 3D UI Design
- Modern gradient-based design with 3D effects
- Responsive layout that works on all devices
- Smooth animations and transitions
- Professional color scheme and typography

### 🤖 AI-Powered Customer Support
- Intelligent conversation flow following Sign-nize's business process
- Warm, professional, and engaging tone
- Handles objections and edge cases gracefully
- Maintains conversation context and history

### 📋 Structured Information Gathering
The system systematically collects:
- Customer identity confirmation
- Sign specifications (size, dimensions, material)
- Installation requirements (surface type, indoor/outdoor)
- Timeline and deadline requirements
- Budget considerations
- Logo and design preferences
- Delivery location details

### 💬 Interactive Features
- Real-time chat interface
- Quick action buttons for common requests
- Typing indicators and loading states
- Message history and session management
- Minimize/maximize functionality

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ChromaDocBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the system**
   Open your browser and navigate to `http://localhost:5000`

## System Architecture

### Backend (Flask)
- **app.py**: Main Flask application with Sign-nize system prompt
- **environment.py**: Environment variable management
- Session management for conversation history
- OpenAI GPT-4 integration for intelligent responses

### Frontend (HTML/CSS/JavaScript)
- **templates/index.html**: Modern 3D UI interface
- **static/style.css**: Professional styling with CSS variables
- **static/script.js**: Interactive functionality and API communication

## Conversation Flow

The AI follows a structured conversation flow:

1. **Introduction & Permission**: Greet customer and confirm availability
2. **Identity Confirmation**: Verify customer identity
3. **Permission to Continue**: Ensure customer is ready to proceed
4. **Information Gathering**: Systematic collection of sign requirements:
   - Size & dimensions
   - Material preferences
   - Installation surface
   - Timeline/deadline
   - Indoor/outdoor placement
   - City and state
   - Permit assistance needs
   - Budget range
   - Logo/design requirements
5. **Wrap-up**: Summarize requirements and confirm next steps

## Key Features

### Professional Tone Management
- Adjusts tone based on customer communication style
- Uses appropriate slang words for casual conversations
- Maintains professionalism for business interactions

### Edge Case Handling
- Busy customers: Offers callback scheduling
- Unavailable customers: Leaves messages with others
- Pricing questions: Redirects to design confirmation first
- Uncertain details: Provides recommendations

### Technical Features
- Session persistence across conversations
- Real-time message processing
- Error handling and recovery
- Responsive design for all screen sizes
- Accessibility considerations

## Customization

### Branding
- Update colors in CSS variables (`:root` section)
- Replace logo and branding elements
- Modify company information in the system prompt

### Conversation Flow
- Edit the `SIGN_NIZE_SYSTEM_PROMPT` in `app.py`
- Adjust question sequences and timing
- Modify response templates and tone

### UI/UX
- Customize CSS variables for different color schemes
- Modify animations and transitions
- Add new quick action buttons

## API Endpoints

- `GET /`: Main chat interface
- `POST /chat`: Send and receive messages
- `GET /chat/<session_id>/history`: Get conversation history
- `DELETE /chat/<session_id>/clear`: Clear session
- `GET /sessions`: List active sessions

## Requirements

- Python 3.8+
- Flask
- OpenAI API key
- Modern web browser

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For technical support or questions about the Sign-nize customer support system, please contact the development team.

---

**Sign-nize** - Custom Sign Design & Production Excellence
