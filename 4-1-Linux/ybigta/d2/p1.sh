# 1. requirements.txt에 있는 Python 패키지 중 설치되지 않은 것이 있다면 설치
#sudo apt-get install -y python3-numpy python3-pandas cowsay
pip install -r requirements.txt

# 2. 현재 실행 중인 process 중 check.py가 있다면 해당 process를 종료
pkill -f check.py

# 3. 자신의 tmux 세션 이름을 선언하고, 해당 세션과 같은 이름의 세션이 없다면 생성
SESSION_NAME="my_tmux_session"

if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
	    tmux new-session -d -s $SESSION_NAME
else
    echo "Session $SESSION_NAME already exists"
fi

# 4. 해당 tmux 세션에서 check.py 를 실행
tmux attach-session -t $SESSION_NAME \; send-keys "python3 check.py" C-m



