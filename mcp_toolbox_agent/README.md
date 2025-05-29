

[ADK와 MCP Toolbox for Databases를 사용한 DB Agent 개발](https://velog.io/@minbrok/ADK와-MCP-Toolbox-for-Databases를-사용한-DB-Agent-개발-s7mhx8wg)

```bash
curl -O https://storage.googleapis.com/genai-toolbox/v0.4.0/linux/amd64/toolbox
```

```zsh
go install github.com/googleapis/genai-toolbox@v0.6.0

$HOME/go/bin/genai-toolbox --tools-file="tools.yaml" --address 0.0.0.0 --port 7000
```

```zsh
lsof -PiTCP -sTCP:LISTEN
netstat -anvp tcp | awk 'NR<3 || /LISTEN/'
```

http://127.0.0.1:8000/api/toolset

```json
{
    "serverVersion":"0.6.0",
    "tools":{
        "get_businesses_by_area":{"description":"지정된 지역(location)에 있는 숙박업소의 목록을 반환합니다.","parameters":[{"name":"location","type":"string","description":"조회할 지역 이름","authSources":[]}],"authRequired":[]},
        "get_businesses_by_year":{"description":"지정된 연도(year)에 승인된 숙박업소 수를 연도별로 집계합니다.","parameters":[{"name":"year","type":"integer","description":"승인 연도","authSources":[]}],"authRequired":[]},
        "get_employee_count_by_category":{"description":"지정된 업종(category)의 평균 직원 수(남여 합산)을 반환합니다.","parameters":[{"name":"category","type":"string","description":"조회할 업종명","authSources":[]}],"authRequired":[]},
        "get_room_stats_by_area":{"description":"지정된 지역(location)의 객실 수(한옥실, 양실) 평균을 계산합니다.","parameters":[{"name":"location","type":"string","description":"객실 통계를 조회할 지역 이름","authSources":[]}],"authRequired":[]}
    }
}
```

```
pip install toolbox-core
```

```zsh
adk web
```

서울의 숙박업소 목록을 보여줘

```
{"error": "module 'aaaa' has no attribute 'agent'"}
{"error": "No module named 'toolbox_core'"}
```