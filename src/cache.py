"""
Simple in-memory caching system for API responses
Improves performance by caching frequently accessed data
"""

import time
import logging
from functools import wraps
from typing import Any, Optional, Callable
import hashlib
import json

logger = logging.getLogger(__name__)


class SimpleCache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self, ttl: int = 300, max_size: int = 100):
        """
        Initialize cache
        
        Args:
            ttl (int): Time to live in seconds (default: 300)
            max_size (int): Maximum number of items in cache (default: 100)
        """
        self.cache = {}
        self.ttl = ttl
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
        logger.info(f"Cache initialized with TTL={ttl}s, max_size={max_size}")
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = {
            'args': args,
            'kwargs': kwargs
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key (str): Cache key
            
        Returns:
            Optional[Any]: Cached value or None if not found/expired
        """
        if key in self.cache:
            value, timestamp = self.cache[key]
            
            # Check if expired
            if time.time() - timestamp < self.ttl:
                self.hits += 1
                logger.debug(f"Cache hit for key: {key}")
                return value
            else:
                # Remove expired entry
                del self.cache[key]
                logger.debug(f"Cache expired for key: {key}")
        
        self.misses += 1
        logger.debug(f"Cache miss for key: {key}")
        return None
    
    def set(self, key: str, value: Any) -> None:
        """
        Set value in cache
        
        Args:
            key (str): Cache key
            value (Any): Value to cache
        """
        # Implement simple LRU by removing oldest if at max size
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
            logger.debug(f"Cache full, removed oldest key: {oldest_key}")
        
        self.cache[key] = (value, time.time())
        logger.debug(f"Cached value for key: {key}")
    
    def delete(self, key: str) -> None:
        """
        Delete value from cache
        
        Args:
            key (str): Cache key
        """
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Deleted cache key: {key}")
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info("Cache cleared")
    
    def get_stats(self) -> dict:
        """
        Get cache statistics
        
        Returns:
            dict: Cache statistics
        """
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.2f}%",
            'ttl': self.ttl
        }
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired entries
        
        Returns:
            int: Number of entries removed
        """
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if current_time - timestamp >= self.ttl
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
        
        return len(expired_keys)


# Global cache instance
_cache = SimpleCache()


def cached(ttl: Optional[int] = None):
    """
    Decorator to cache function results
    
    Args:
        ttl (int, optional): Time to live in seconds (uses default if not specified)
        
    Example:
        @cached(ttl=300)
        def expensive_function(arg1, arg2):
            # ... expensive computation
            return result
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{_cache._generate_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_value = _cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            
            # Use custom TTL if provided
            if ttl is not None:
                old_ttl = _cache.ttl
                _cache.ttl = ttl
                _cache.set(cache_key, result)
                _cache.ttl = old_ttl
            else:
                _cache.set(cache_key, result)
            
            return result
        
        return wrapper
    return decorator


def get_cache() -> SimpleCache:
    """Get the global cache instance"""
    return _cache


def clear_cache() -> None:
    """Clear the global cache"""
    _cache.clear()


def get_cache_stats() -> dict:
    """Get global cache statistics"""
    return _cache.get_stats()


# Example usage
if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Create cache
    cache = SimpleCache(ttl=5, max_size=3)
    
    # Test basic operations
    print("Testing cache operations...")
    
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    
    print(f"Get key1: {cache.get('key1')}")
    print(f"Get key2: {cache.get('key2')}")
    print(f"Get key3: {cache.get('key3')}")
    
    print(f"\nCache stats: {cache.get_stats()}")
    
    # Test TTL
    print("\nWaiting 6 seconds for TTL expiration...")
    time.sleep(6)
    print(f"Get key1 after expiration: {cache.get('key1')}")
    
    print(f"\nFinal cache stats: {cache.get_stats()}")
    
    # Test decorator
    @cached(ttl=10)
    def expensive_function(x, y):
        print(f"Computing {x} + {y}...")
        time.sleep(1)
        return x + y
    
    print("\n\nTesting cached decorator...")
    print(f"First call: {expensive_function(5, 3)}")
    print(f"Second call (cached): {expensive_function(5, 3)}")
    print(f"Different args: {expensive_function(10, 20)}")
    
    print(f"\nDecorator cache stats: {get_cache_stats()}")
