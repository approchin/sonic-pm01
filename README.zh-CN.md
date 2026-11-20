# SONIC-PM01

这是面向众擎 PM01 的独立 SONIC 适配研究工程。仓库提供 Actor 推理源码、模型接口和仿真结果。

## 先看什么

- [总体、Actor、Critic 三张架构图](docs/architecture.md)
- [实验结果、误差指标与判据](docs/evaluation.md)
- [权重下载与使用说明](docs/weights.md)
- [历史训练配方](docs/training_recipe.md)
- [能力范围与局限](docs/limitations.md)

## A/B 分别训练了什么

| 版本 | Actor 中的 Encoder | Actor 中的 Decoder | Critic |
|---|---|---|---|
| A | 冻结 | 训练 | 训练 |
| B | 训练 | 训练 | 训练 |

两路都是稠密微调，不是 LoRA。Encoder、FSQ 和 Decoder 构成实际使用的 SONIC 追踪分支；Decoder 本来就属于 Actor。推理输出身体23维动作均值，头部另走参考PD。Critic只在训练时估计价值。

## 权重

A、B 各有 4k 和 28k 两份权重。4k是低算力节点（A约6.514、B约6.712个RTX4090训练进程卡时），28k是已有配套评测、追踪误差更低的后期对照。90小时和未完成的后训练版本不借用这些成绩。

| 固定仿真测试 | A 4k | B 4k | A 28k | B 28k |
|---|---:|---:|---:|---:|
| OMOMO394＋LAFAN106 | 97.0% | 96.6% | 97.0% | 97.0% |
| BONES500 | 99.6% | 99.6% | 99.6% | 99.6% |

完成率不是跟踪精度；完整关节误差、位置误差、分母及比较范围见实验说明。这里的“未见”仅指对应录制未用于PM01适配训练，不能证明SONIC预训练没见过有关数据。测试名单有历史曝光，BONES同源库动作家族也有重叠；当前是固定种子的本地论文启发判据，不是Any2Any原官方平台，也不据此宣称“一半算力全面优于Any2Any”。

## 发布范围

权重为 Actor 的 ONNX 和 safetensors 推理导出，附输入格式、关节顺序、后处理与最小CPU前向示例。它们不包含Critic、优化器和采样器等完整续训状态，也不构成已验证的实机闭环控制器。原始完整检查点仍单独保留。

Motion Data by [Bones Studio](https://bones.studio/)。使用主体已确认为学校／科研机构的非商业研究；模型、代码、机器人资产与原始动作数据分别遵循相应条款，详见[许可与出处](docs/licensing.md)。
