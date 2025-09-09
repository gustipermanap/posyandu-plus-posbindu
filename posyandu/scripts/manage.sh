#!/bin/bash

# Script utama untuk mengelola semua services Posyandu+ dan POS BINDU PTM

echo "🎛️  Posyandu+ & POS BINDU PTM Management"
echo "========================================"

# Function untuk show menu
show_menu() {
    echo ""
    echo "🎛️  Available Commands:"
    echo "======================"
    echo ""
    echo "🚀 Service Management:"
    echo "  1. start     - Start all services"
    echo "  2. stop      - Stop all services"
    echo "  3. restart   - Restart all services"
    echo "  4. status    - Check status of all services"
    echo "  5. test      - Test all services"
    echo ""
    echo "📋 Logs & Monitoring:"
    echo "  6. logs      - View logs for all services"
    echo "  7. logs [service] - View logs for specific service"
    echo ""
    echo "🧹 Cleanup:"
    echo "  8. cleanup   - Full cleanup (stop + clean all)"
    echo "  9. cleanup --stop - Stop all services only"
    echo "  10. cleanup --images - Clean images only"
    echo ""
    echo "🆘 Help:"
    echo "  11. help     - Show help"
    echo "  12. help --services - Show available services"
    echo "  13. help --examples - Show usage examples"
    echo ""
    echo "🌐 Quick Access:"
    echo "  📱 Posyandu+ Frontend: http://localhost:3000"
    echo "  🔗 Posyandu+ API: http://localhost"
    echo "  📱 POS BINDU PTM Frontend: http://localhost:3001"
    echo "  🔗 POS BINDU PTM API: http://localhost:8080"
    echo ""
    echo "🔑 Demo Login: admin / admin123"
    echo ""
}

# Function untuk execute command
execute_command() {
    local command=$1
    local service=$2
    
    case "$command" in
        start)
            echo "🚀 Starting all services..."
            ./start_all.sh
            ;;
        stop)
            echo "🛑 Stopping all services..."
            ./stop_all.sh
            ;;
        restart)
            echo "🔄 Restarting all services..."
            ./restart_all.sh
            ;;
        status)
            echo "📊 Checking status..."
            ./status_all.sh
            ;;
        test)
            echo "🧪 Testing all services..."
            ./test_all.sh
            ;;
        logs)
            if [ -n "$service" ]; then
                echo "📋 Viewing logs for $service..."
                ./logs_all.sh "$service"
            else
                echo "📋 Viewing logs for all services..."
                ./logs_all.sh
            fi
            ;;
        cleanup)
            if [ "$service" = "--stop" ]; then
                echo "🛑 Stopping all services..."
                ./stop_all.sh
            elif [ "$service" = "--images" ]; then
                echo "🧹 Cleaning images..."
                ./cleanup_all.sh --images
            else
                echo "🧹 Full cleanup..."
                ./cleanup_all.sh
            fi
            ;;
        help)
            if [ "$service" = "--services" ]; then
                echo "📋 Showing available services..."
                ./help_all.sh --services
            elif [ "$service" = "--examples" ]; then
                echo "💡 Showing usage examples..."
                ./help_all.sh --examples
            else
                echo "🆘 Showing help..."
                ./help_all.sh
            fi
            ;;
        *)
            echo "❌ Unknown command: $command"
            echo "Use 'help' to see available commands"
            return 1
            ;;
    esac
}

# Function untuk interactive mode
interactive_mode() {
    while true; do
        show_menu
        echo -n "Enter command (or 'quit' to exit): "
        read -r input
        
        # Parse input
        IFS=' ' read -r command service <<< "$input"
        
        # Check for quit
        if [ "$command" = "quit" ] || [ "$command" = "exit" ] || [ "$command" = "q" ]; then
            echo "👋 Goodbye!"
            break
        fi
        
        # Execute command
        if [ -n "$command" ]; then
            execute_command "$command" "$service"
        else
            echo "❌ Please enter a command"
        fi
        
        echo ""
        echo "Press Enter to continue..."
        read -r
    done
}

# Function untuk show help
show_help() {
    echo "🎛️  Posyandu+ & POS BINDU PTM Management"
    echo "========================================"
    echo ""
    echo "Usage:"
    echo "  ./manage.sh                    # Interactive mode"
    echo "  ./manage.sh [command] [option]  # Direct command execution"
    echo ""
    echo "Commands:"
    echo "  start                          # Start all services"
    echo "  stop                           # Stop all services"
    echo "  restart                        # Restart all services"
    echo "  status                         # Check status of all services"
    echo "  test                           # Test all services"
    echo "  logs [service]                 # View logs (all or specific service)"
    echo "  cleanup [option]               # Cleanup (full, --stop, --images)"
    echo "  help [option]                  # Show help (--services, --examples)"
    echo ""
    echo "Examples:"
    echo "  ./manage.sh start              # Start all services"
    echo "  ./manage.sh logs auth-service  # View auth-service logs"
    echo "  ./manage.sh cleanup --images   # Clean images only"
    echo "  ./manage.sh help --services    # Show available services"
    echo ""
    echo "Interactive Mode:"
    echo "  ./manage.sh                    # Start interactive mode"
    echo ""
}

# Main execution
main() {
    # Check for help flag
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_help
        return 0
    fi
    
    # Check if command is provided
    if [ -n "$1" ]; then
        # Direct command execution
        execute_command "$1" "$2"
    else
        # Interactive mode
        interactive_mode
    fi
}

# Run main function
main "$@"
