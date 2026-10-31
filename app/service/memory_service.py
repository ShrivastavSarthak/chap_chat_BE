from cachetools import TTLCache


guest_memory_cache: TTLCache[str, list[dict[str,str]]] = TTLCache(maxsize=1000,ttl=300)

def get_guest_history(guest_id: str) ->list[dict[str,str]]:
    return guest_memory_cache.get(guest_id,[])

def append_guest_dialogue(guest_id:str, user_msg:str, assistant_msg:str) -> None:
    history = guest_memory_cache.get(guest_id,[])
    history.append({"role":"user", "content":user_msg})
    history.append({"role":"assistant", "content":assistant_msg})
    
    guest_memory_cache[guest_id] = history[-20:]