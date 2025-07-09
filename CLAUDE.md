# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

bitchat is a secure, decentralized peer-to-peer messaging application that operates over Bluetooth Low Energy (BLE) mesh networks. It provides end-to-end encrypted communication without internet infrastructure, making it resilient to network outages and censorship.

## Development Commands

### Project Setup
```bash
# Install XcodeGen (recommended)
brew install xcodegen

# Generate Xcode project
xcodegen generate

# Open project
open bitchat.xcodeproj
```

### Alternative Setup Methods
```bash
# Using Swift Package Manager
open Package.swift

# Manual setup script
./setup.sh
```

### Testing
```bash
# Run tests in Xcode
# - Select Test scheme
# - Cmd+U to run all tests

# Test files located in bitchatTests/:
# - BinaryProtocolTests.swift
# - BitchatMessageTests.swift  
# - BloomFilterTests.swift
# - MessagePaddingTests.swift
# - PasswordProtectedChannelTests.swift
```

## Architecture Overview

### Core Components

**Application Layer**
- `BitchatApp.swift` - Main app entry point with SwiftUI App lifecycle
- `ContentView.swift` - Primary chat interface
- `ChatViewModel.swift` - Core view model managing chat state and user interactions

**Protocol Layer**
- `BitchatProtocol.swift` - Core protocol definitions, message types, and data structures
- `BinaryProtocol.swift` - Efficient binary serialization for BLE transmission

**Services Layer**
- `BluetoothMeshService.swift` - BLE mesh networking implementation
- `EncryptionService.swift` - X25519 key exchange and AES-256-GCM encryption
- `MessageRetryService.swift` - Message delivery retry logic
- `MessageRetentionService.swift` - Channel message persistence
- `DeliveryTracker.swift` - Message delivery confirmation tracking
- `NotificationService.swift` - Push notification handling

**Utilities**
- `CompressionUtil.swift` - LZ4 message compression
- `OptimizedBloomFilter.swift` - Duplicate message detection
- `BatteryOptimizer.swift` - Power-aware networking modes
- `KeychainManager.swift` - Secure key storage

### Key Architecture Patterns

**Mesh Networking**: Each device acts as both BLE central and peripheral, enabling multi-hop message relay with TTL-based routing.

**Store-and-Forward**: Messages are cached when recipients are offline, with tiered retention (12hrs for regular peers, indefinite for favorites).

**Dual Protocol Support**: Binary protocol for efficient BLE transmission, with JSON fallback for debugging.

**Power Management**: Adaptive networking based on battery state (Performance, Balanced, Power Saver, Ultra Low Power modes).

## Security Model

### Encryption Layers
- **Private Messages**: X25519 ECDH key exchange + AES-256-GCM
- **Channel Messages**: Argon2id password derivation + AES-256-GCM  
- **Message Integrity**: Ed25519 digital signatures
- **Forward Secrecy**: New key pairs generated each session

### Privacy Features
- **Ephemeral Identities**: Random peer IDs per session
- **Cover Traffic**: Dummy messages to prevent traffic analysis
- **Timing Randomization**: 50-500ms delays on operations
- **Emergency Wipe**: Triple-tap to clear all data

## Development Notes

### Platform Support
- iOS 16.0+ and macOS 13.0+
- Universal app supporting iPhone, iPad, and Mac
- Share extension for external content sharing

### Testing Requirements
- **Physical Devices Only**: Bluetooth functionality requires real hardware
- **Multiple Devices**: Test mesh networking with 2+ devices
- **Bluetooth Enabled**: Ensure Bluetooth is enabled in device settings

### Code Organization
- Swift 5.0+ with SwiftUI for UI
- Combine framework for reactive programming
- CoreBluetooth for BLE mesh networking
- CryptoKit for encryption operations
- No external dependencies beyond Apple frameworks

### Message Flow
1. User input → ChatViewModel
2. Encryption → EncryptionService
3. Compression → CompressionUtil (if >100 bytes)
4. Fragmentation → BinaryProtocol (if >500 bytes)
5. Transmission → BluetoothMeshService
6. Mesh Relay → TTL-based routing
7. Store-and-Forward → MessageRetentionService (if recipient offline)

### CLI Tool
A command-line interface is available in `bitchat-cli/` for protocol testing and debugging.

## Performance Considerations

### Message Optimization
- LZ4 compression for messages >100 bytes (30-70% size reduction)
- Automatic fragmentation for messages >500 bytes
- Bloom filters for efficient duplicate detection

### Battery Optimization
- Adaptive scanning duty cycles based on battery level
- Connection limits vary by power mode (2-20 connections)
- Advertising interval adjustments (3s-30s based on battery)

### Network Efficiency
- Binary protocol minimizes BLE packet overhead
- Message aggregation reduces transmission frequency
- Optimized connection management for BLE constraints