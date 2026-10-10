# Universal Behavioral Action Tags

Poly-Scan operates by mapping language-specific syntax into language-agnostic Universal Tags. This allows true apple-to-apple behavioral comparisons.

## V1 Mappings

### `[EXEC_SYS_CMD]`
Executes a system-level shell command.
- **Python**: `os.system`
- **JavaScript**: `child_process.exec`

### `[PROCESS_EXEC]`
Spawns a sub-process or binary executable (usually without a full shell context).
- **Python**: `subprocess.*`
- **JavaScript**: `child_process.spawn`

### `[FILE_WRITE]`
Opens a file handler with write/append permissions and mutates disk data.
- **Python**: `open(..., 'w' | 'a' | 'x' | '+')`
- **JavaScript**: `fs.writeFileSync`, `fs.createWriteStream`

### `[FILE_READ]`
Opens a file handler with read-only permissions.
- **Python**: `open(...)` (without write modes)
- **JavaScript**: *(To be implemented in V2)*

### `[NET_OUTBOUND]`
Initiates an outbound network connection.
- **Python**: `socket.connect`, `*.connect`
- **JavaScript**: `net.createConnection`, `*.connect`

### `[DECODE_PAYLOAD]`
Decodes data, typically used in obfuscated malware delivery.
- **Python**: `base64.b64decode`
- **JavaScript**: `Buffer.from(..., 'base64')`

### `[UNKNOWN]`
Any parsed AST node call that does not match the known mapping dictionary. Ignored in similarity calculations.
