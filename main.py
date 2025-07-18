"""
系统入口：负责接收输入并执行主推理流程
"""
import argparse
from typing import Optional, Dict, Any
from config import Config
from agent.main_agent import MainAgent


class MultiAgentResearchSystem:
    """多智能体深度研究系统主类"""
    
    def __init__(self):
        """初始化系统"""
        self.config = Config()
        self.main_agent = MainAgent()
        
    def research_query(self, query: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        处理研究查询
        
        Args:
            query: 用户查询
            context: 可选的上下文信息
            
        Returns:
            包含答案、引用和推理轨迹的字典
        """
        try:
            # 使用主Agent执行ReAct推理
            result = self.main_agent.execute_reasoning(query, context)
            
            print("✅ 查询处理完成")
            return result
            
        except Exception as e:
            print(f"❌ 处理查询时出错: {str(e)}")
            return {
                "answer": f"处理查询时出现错误: {str(e)}",
                "citations": [],
                "reasoning_trace": "",
                "error": True
            }
    
    def interactive_mode(self):
        """交互模式"""
        print("🤖 多智能体深度研究系统启动")
        print("输入 'quit' 或 'exit' 退出系统")
        print("输入 'reset' 重置对话")
        print("-" * 50)
        
        while True:
            try:
                query = input("\n请输入您的研究问题: ").strip()
                
                if query.lower() in ['quit', 'exit', '退出']:
                    print("👋 感谢使用，再见！")
                    break

                if query.lower() == 'reset':
                    print("🔄 重置对话")
                    self.main_agent.reset_session()
                    continue

                if not query:
                    continue
                
                # 处理查询
                result = self.research_query(query)
                
                # 显示结果
                print("\n" + "="*60)
                print("📋 研究结果:")
                print("="*60)
                print(f"\n💡 答案: {result['answer']}")
                if result.get('reasoning_trace'):
                    print(f"\n🧠 推理过程:")
                    print(result['reasoning_trace'])

                if result.get('citations'):
                    print(f"\n📚 参考链接:")
                    for i, citation in enumerate(result['citations'], 1):
                        print(f"  [{i}] {citation}")
                
            except KeyboardInterrupt:
                print("\n\n👋 用户中断，退出系统")
                break
            except Exception as e:
                print(f"\n❌ 系统错误: {str(e)}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="多智能体深度研究系统")
    parser.add_argument("--mode", choices=["interactive"], 
                       default="interactive", help="运行模式")
    parser.add_argument("--query", type=str, 
                       help="单次查询（非交互模式）")
    
    args = parser.parse_args()
    
    system = MultiAgentResearchSystem()
    
    if args.mode == "interactive":
        if args.query:
            # 单次查询模式
            result = system.research_query(args.query)
            print(f"答案: {result['answer']}")
            if result.get('citations'):
                print("引用:")
                for citation in result['citations']:
                    print(f"  - {citation}")
        else:
            # 交互模式
            system.interactive_mode()


if __name__ == "__main__":
    main()
