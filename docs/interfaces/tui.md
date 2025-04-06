# AskDocs Text User Interface (TUI)

AskDocs provides a rich terminal interface using the Textual framework, offering a full-screen interactive experience.

## Features

- Full-screen interactive terminal interface
- Keyboard shortcuts for quick navigation
- Dark mode toggle
- Integrated knowledge base management
- Real-time status indicators
- Cross-platform compatibility

## Starting the TUI

```bash
# Launch the TUI application
askdocs tui
```

## Interface Components

### Question Input Panel

- Text input field for entering questions
- Model selection dropdown
- Template selection dropdown
- Ask button
- Preview button

### Results Display

- Renders the answer with rich formatting
- Shows source documents used to generate the answer
- Displays confidence metrics

### Knowledge Base Panel

- Shows knowledge base statistics
- Provides option to rebuild knowledge base
- Indicates whether embeddings are being used

### Settings Panel

- Toggle dark mode
- Change model settings
- Adjust document retrieval parameters

## Keyboard Shortcuts

| Key | Action |
| --- | --- |
| `Tab` | Navigate between input fields |
| `Enter` | Submit current form |
| `Ctrl+Q` | Quit the application |
| `Ctrl+D` | Toggle dark mode |
| `Ctrl+R` | Rebuild knowledge base |
| `Ctrl+P` | Preview document matches |
| `F1` | Show help |

## Customization

### Styling

The TUI interface can be customized by modifying the CSS in `askdocs/tui/style.css`. This allows you to change colors, layout, and other visual aspects.

Example modifications:

```css
/* Change the background color in light mode */
Screen {
    background: #f5f5f5;
}

/* Change the header text color */
Header {
    color: #2d79c7;
}
```

### Configuration

The TUI uses the same configuration system as the rest of AskDocs. You can adjust settings through `config.json` or environment variables:

```json
{
  "tui": {
    "dark_mode": true,
    "show_status_bar": true
  }
}
```

## Advanced Usage

### Working with Large Terminal Windows

The TUI is designed to be responsive and will adapt to the size of your terminal window. For the best experience, use a terminal with at least 80x24 characters.

### Custom Color Schemes

You can create custom color schemes by modifying the CSS variables in `style.css`:

```css
:root {
    --primary: #2d79c7;
    --secondary: #6c757d;
    --success: #28a745;
    --warning: #ffc107;
    --error: #dc3545;
}
```

### Using in Different Terminals

The TUI works in most modern terminal emulators, including:
- iTerm2
- Windows Terminal
- GNOME Terminal
- Alacritty
- Kitty

Some terminals may have better support for rich text features and colors than others.