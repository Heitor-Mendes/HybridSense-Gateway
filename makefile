# Nome do executável final
TARGET = programa.exe

# Diretórios
SRC_DIR = sistema/src
INC_DIR = sistema/include
OBJ_DIR = obj

# Compilador e Flags
CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -I$(INC_DIR)

# Bibliotecas de linkedição
LDFLAGS = -lws2_32

# Procura automaticamente por todos os arquivos .cpp na pasta src
SRCS = $(wildcard $(SRC_DIR)/*.cpp)

# Define os arquivos .o equivalentes dentro da pasta obj/
OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRCS))

# Regra principal
all: $(TARGET)

# Regra para linkar os objetos e gerar o executável
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

# Regra para compilar cada arquivo .cpp em um .o
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@if not exist $(OBJ_DIR) mkdir $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Regra para limpar os arquivos gerados no Windows
clean:
	@if exist $(OBJ_DIR) rmdir /s /q $(OBJ_DIR)
	@if exist $(TARGET) del /q $(TARGET)

.PHONY: all clean