data_login = {
    "jsonrpc": "2.0",
    "id": 0,
    "method": "get",
    "params": [
        {
            "session_id": "00000000000000000000000000000000"
        },
        {
            "dest": "login"
        }
        # {
        #     "data": {
        #         "username": "c8c4c4c9c7",
        #         "password": "9090909090"
        #     }
        # }
    ]
}

get_conf = {
    "jsonrpc": "2.0",
    "id": 0,
    "method": "get",
    "params": [
        {
            "session_id": "9763fe5318c46cf03ba0c11196192a99"
        },
        {
            "dest": "mwans"
        },
        {
            "data": []
        }
    ]
}


set_pass ={
    "jsonrpc": "2.0",
    "id": 0,
    "method": "set",
    "params": [
        {
            "session_id": "a28639bc0a8fc501efc2be03443c6bf6"
        },
        {
            "dest": "password"
        }
    ]
}

wlan = {
    "jsonrpc": "2.0",
    "id": 0,
    "method": "set",
    "params": [
        {
            "session_id": "4476a94d78e9abf9df7e53c7a0148c59"
        },
        {
            "dest": "mwans"
        }

    ]
}