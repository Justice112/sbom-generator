# 软件物料清单生成工具

该工具用于生成软件物料清单 Excel 文件，以帮助用户跟踪软件项目中使用的各种组件及其相关信息。

## 如何使用

1. **安装依赖**：

   请确保已安装以下 Python 包：

   - `openpyxl`: 用于处理 Excel 文件。
   - `pyInstaller`: 用于将 Python 程序打包成可执行文件。

   你可以通过以下命令安装依赖：

   ```shell
   pip install openpyxl
   pip install pyInstaller
   ```

2. **运行程序**：

运行 `python main.py` 文件以启动 GUI 界面。在界面中输入 `package-lock.json` 文件路径和要保存的 Excel 文件路径及名称，然后点击“保存并打开文件”按钮。程序将生成软件物料清单 Excel 文件，并询问是否打开该文件。

## 文件结构

- `main.py`: 主程序文件，包含打包和运行逻辑。
- `main.spec`: PyInstaller 配置文件，用于指定打包选项。
- `db/packages_v2.db`: 数据库文件，用于存储依赖包信息。
- `db/package_info_db_v2.py`: 数据库操作模块。
- `src/sbom_builder.py`: 用于生成 sbom 文件的模块。
- `src/parser/package_lock_parser_v2.py`: 解析 `package-lock.json` 文件的模块。

## 贡献

欢迎提出问题和改进建议！如果你发现了 bug 或者有新功能的想法，请提交一个 issue 或者发送一个 Pull Request。

## 许可证

该项目基于 MIT 许可证。请参阅 [LICENSE](LICENSE) 文件获取更多信息。

## 注意事项

- 确保输入的 `package-lock.json` 文件路径正确，并且文件格式符合预期。
- 如果程序报错或者无法生成 Excel 文件，请检查是否安装了正确的依赖库，并且检查 `package-lock.json` 文件是否包含了正确的数据。
- 由于程序依赖于 `openpyxl` 库，因此请确保该库已正确安装。
- 激活虚拟环境：venv\Scripts\activate

  3.**打包程序**
  你可以通过以下命令打包程序：

      ```shell
          pyinstaller main.py --onefile --name=SBOMGenerator_v2.0 --icon=sbom.ico
      ```
