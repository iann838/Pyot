# Exceptions

List of exceptions that Pyot uses.

Module: `pyot.core.exceptions`

### _class_ PyotException
Extends: `Exception`

Base Pyot exception class.

### _class_ NotFindable
Extends: `PyotException`

Message: [600] Pipeline token matching pair not found

### _class_ SessionNotFound
Extends: `PyotException`

Message: [601] Session Not Found.

### _class_ DecodeError
Extends: `PyotException`

Message: [602] AioHttp took too long to decode the response.

### _class_ NoContent
Extends: `PyotException`

Message: [204] No Content.

### _class_ NotFound
Extends: `PyotException`

Message: [404] Data Not Found.

### _class_ MethodNotAllowed
Extends: `PyotException`

Message: [405] Method Not Allowed.

### _class_ ServerError
Extends: `PyotException`

Messages: `Mapping[int, str]`
  * 500: Internal Server Error
  * 502: Bad Gateway
  * 503: Service Unavailable
  * 504: Gateway Timeout
[{code}] {self.messages[code]}.

### _class_ RateLimited
Extends: `PyotException`

Message: [429] Rate limit Exceeded.

### _class_ Forbidden
Extends: `PyotException`

Message: [403] Access Forbidden.

### _class_ Unauthorized
Extends: `PyotException`

Message: [401] Access Unauthorized.

### _class_ BadRequest
Extends: `PyotException`

Message: [400] Bad Request.

### _class_ Timeout
Extends: `PyotException`

Message: [408] Timeout Connection.

### _class_ UnidentifiedResponse
Extends: `PyotException`

Message: [{code}] Unidentified Response {code}.


