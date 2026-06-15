<!-- BLOCK: b_001 | type: paragraph -->
综述
<!-- BLOCK_END: b_001 -->

<!-- BLOCK: b_002 | type: heading | heading: Object Detection with Transformers: A Review -->
# 基于Transformers的目标检测：综述
<!-- BLOCK_END: b_002 -->

<!-- BLOCK: b_003 | type: paragraph | heading: Object Detection with Transformers: A Review -->
Tahira Shehzadi 1,2,3,\* , Khurram Azeem Hashmi 1,2,3 , Marcus Liwicki 4 , Didier Stricker 1,2,3 和 Muhammad Zeshan Afzal 1,2,3 凯泽斯劳滕工业大学计算机科学系，67663 凯泽斯劳滕，德国；muhammad\_zeshan.afzal@dfki.de (M.Z.A.) 2 Mindgarage实验室，凯泽斯劳滕工业大学，67663 凯泽斯劳滕，德国 3 德国人工智能研究中心（DFKI），67663 凯泽斯劳滕，德国 4 吕勒奥理工大学计算机科学、电气与空间工程系，971 87 吕勒奥，瑞典 通讯作者：tahira.shehzadi@dfki.de
<!-- BLOCK_END: b_003 -->

<!-- BLOCK: b_009 | type: heading | heading: Object Detection with Transformers: A Review > Abstract -->
## 摘要
<!-- BLOCK_END: b_009 -->

<!-- BLOCK: b_010 | type: abstract | heading: Object Detection with Transformers: A Review > Abstract -->
Transformer在自然语言处理（NLP）中的卓越表现激励研究人员探索其在计算机视觉任务中的应用。
检测Transformer（DETR）通过将检测重新定义为集合预测问题，将Transformer引入目标检测任务。
因此，它消除了对提议生成和后处理步骤的需求。
尽管具有有竞争力的性能，DETR最初面临训练收敛缓慢和小目标检测性能不佳的问题。
然而，大量改进方案被提出以解决这些问题，取得了显著进步，使DETR能够达到最先进的性能。
据我们所知，本文是首次对25项近期DETR进展进行全面综述。
我们深入探讨了DETR的基础模块及其最新增强，包括骨干结构的修改、查询设计策略以及注意力机制的优化。
此外，我们对多种检测Transformer进行了比较分析，评估了它们的性能和网络架构。
我们希望本研究能够推动进一步研究，以解决现有挑战并探索Transformer在目标检测领域的应用。
<!-- BLOCK_END: b_010 -->

<!-- BLOCK: b_011 | type: figure_caption | heading: Object Detection with Transformers: A Review > Abstract -->
![](Images_GFP684MN/c514bb2c7e1ee2c19c5c48012bc5d813b5a109874e84c32783c402d698515f4e.jpg)
<!-- BLOCK_END: b_011 -->

<!-- BLOCK: b_012 | type: paragraph | heading: Object Detection with Transformers: A Review > Abstract -->
学术编辑：Liang-Jian Deng 收稿日期：2025年8月16日 修回日期：2025年9月24日 接受日期：2025年9月26日 发表日期：2025年10月1日 引用格式：Shehzadi, T.; Hashmi, K.A.; Liwicki, M.; Stricker, D.; Afzal, M.Z. 基于Transformers的目标检测：综述。
Sensors 2025, 25, 6025. https://doi.org/10.3390/s25196025 版权：© 2025 作者所有。
出版方 MDPI，巴塞尔，瑞士。
本文为开放获取文章，依据知识共享署名（CC BY）许可（https://creativecommons.org/lice nses/by/4.0/）的条款和条件分发。
关键词：Transformer；目标检测；DETR；计算机视觉；深度神经网络
<!-- BLOCK_END: b_012 -->

<!-- BLOCK: b_017 | type: heading | heading: Object Detection with Transformers: A Review > 1. Introduction -->
## 1. 引言
<!-- BLOCK_END: b_017 -->

<!-- BLOCK: b_018 | type: paragraph | heading: Object Detection with Transformers: A Review > 1. Introduction -->
目标检测是计算机视觉中的一项基础任务，涉及在图像中定位和分类目标[1–6]，在自动驾驶、监控、机器人和医学影像等领域有广泛应用。
例如，在自动驾驶中，实时准确地检测行人、车辆和交通标志对安全至关重要。
传统上，卷积神经网络（CNN），如faster R-CNN [1]和RetinaNet [4]，一直作为目标检测模型的主要骨干，取得了令人瞩目的性能。
然而，这些模型严重依赖手工设计的组件，如区域提议网络（RPN）和非极大值抑制（NMS）[7]等后处理步骤，这使训练流程复杂化并限制了端到端优化。
Transformer在自然语言处理（NLP）中的近期成功激励研究人员探索其在计算机视觉中的潜力[8]。
Transformer架构[9,10]能够有效捕捉序列数据中的长距离依赖关系，实现传统CNN难以达到的全局上下文建模。
这一能力使Transformer在目标检测中特别有吸引力，因为目标识别往往依赖于全局上下文。
Transformer架构[9,10]以其编码器-解码器结构以及自注意力和交叉注意力机制为特征，使其能够有效捕捉输入序列间的长距离依赖关系。
与主要通过卷积核关注局部特征的CNN不同，Transformer可以对整幅图像中的全局关系进行建模。
这一能力使Transformer特别适用于目标检测，其中理解多个目标之间的空间和上下文关系至关重要。
利用这一优势，研究人员探索了基于Transformer的方法，以开发不依赖手工设计组件的端到端目标检测框架。
在此背景下，Carion等人（2020）提出了检测Transformer（DETR）[11]，这是一种新颖的框架，使用Transformer编码器-解码器网络以端到端可训练的架构取代了传统的基于区域提议的方法。
DETR网络展示了有前景的性能，优于传统的基于CNN的目标检测器[12–19]，同时消除了对区域提议网络和非极大值抑制（NMS）[7]等后处理步骤的需求。
尽管有这些优势，DETR仍存在一些局限性，包括训练收敛缓慢和对小目标的检测性能不佳，这激发了后续研究中的大量修改和改进。
自DETR提出以来，大量变体相继出现，以解决收敛缓慢、小目标检测和计算效率等局限性。
Figure 1展示了DETR研究的发展与演变，显示了论文发表和引用的增长、广泛的架构修改，以及对提高训练稳定性、效率和小目标性能等关键挑战的关注。
这凸显了基于Transformer的检测的快速扩展，强调了进行全面综述的必要性，众多DETR变体已对此作出响应。
Deformable-DETR [20]将注意力模块修改为处理图像特征图，将注意力机制视为训练收敛缓慢的主要原因，而UP-DETR [21]则提出了对DETR进行预训练的修改，类似于自然语言处理中Transformer的预训练。
Efficient-DETR [22]基于原始DETR和Deformable-DETR，考察了随机初始化的目标概率，包括参考点和目标查询，这是多次训练迭代的原因之一。
SMCA-DETR [23]引入了一种空间调制协同注意力模块，取代DETR中现有的协同注意力机制以克服训练收敛缓慢的问题，而TSP-DETR [24]则处理交叉注意力和二分匹配的不稳定性。
Conditional-DETR [25]提出了一种条件交叉注意力机制，而WB-DETR [26]将基于CNN的骨干网络作为额外组件用于特征提取，并提出了一种无骨干网络的Transformer编码器-解码器网络。
PnP-DETR [27]提出了一种PnP采样模块，以减少空间冗余并提高计算效率。
Dynamic-DETR [28]在编码器-解码器网络中引入动态注意力，YOLOS-DETR [29]展示了Transformer从图像识别到检测的可迁移性和通用性，Anchor-DETR [30]将目标查询作为锚点，Sparse-DETR [31]通过令牌过滤降低计算成本，D2ETR [32]在解码器中使用跨尺度注意力，FP-DETR [33]重新制定了预训练和微调，而CF-DETR [34]细化预测位置以改善小目标检测。
针对训练稳定性和小目标性能的进一步改进包括：DN-DETR [35]使用加噪目标查询作为额外解码器输入以减少二分匹配机制的不稳定性，AdaMixer [36]将编码器视为骨干网络和解码器之间的额外网络并引入三维采样过程，REGO-DETR [37]提出了一种基于RoI的检测细化方法，以及DINO [38]使用正负加噪目标查询加速收敛并增强小目标性能。
这些连续的创新共同解决了原始DETR的局限性，同时保留了其作为完全端到端基于Transformer的目标检测器的优势。
FP-DETR [33]重新制定了检测Transformer的预训练和微调阶段。
CF-DETR [34]通过利用局部信息细化预测位置，因为不正确的边界框定位会降低小目标的检测性能。
<!-- BLOCK_END: b_018 -->

<!-- BLOCK: b_022 | type: figure_caption | heading: Object Detection with Transformers: A Review > 1. Introduction -->
![](Images_GFP684MN/e74b6930f314f176ea39cf2a148b08c9ce97a03f02b01c09a6f25c9d994170df.jpg)
<!-- BLOCK_END: b_022 -->

<!-- BLOCK: b_023 | type: figure_caption | heading: Object Detection with Transformers: A Review > 1. Introduction -->
![](Images_GFP684MN/9257ee4fb1bc2d0948731b4d1a12759bbac63a85c778819757fbbeef3222c67c.jpg)
<!-- BLOCK_END: b_023 -->

<!-- BLOCK: b_024 | type: figure_caption | heading: Object Detection with Transformers: A Review > 1. Introduction -->
![](Images_GFP684MN/e2b186443539d9f00a83527d7bd004200983b49fa17f50cd39f199a34f1f416c.jpg)
<!-- BLOCK_END: b_024 -->

<!-- BLOCK: b_025 | type: figure_caption | heading: Object Detection with Transformers: A Review > 1. Introduction -->
![](Images_GFP684MN/2eae80c82c80c0911466e8740e86190d34c5ab17823279e98b99313153edcacf.jpg)
<!-- BLOCK_END: b_025 -->

<!-- BLOCK: b_026 | type: figure_caption | heading: Object Detection with Transformers: A Review > 1. Introduction -->
(e) 检测Transformer（DETR）重要发展时间线
<!-- BLOCK_END: b_026 -->

<!-- BLOCK: b_027 | type: figure_caption | heading: Object Detection with Transformers: A Review > 1. Introduction -->
![](Images_GFP684MN/89d759034494e7cb0ef369187dd866546fdd7b63c1f2fae502d3b1ac6d807af8.jpg) Figure 1。
Transformer文献的统计概览。(a) 各年度Transformer论文的引用次数。(b) 最近12个月内检测Transformer论文的引用次数。(c) 原始检测Transformer（DETR）中为提升性能和收敛速度所作的修改比例。(d) 各年度以DETR为基线的同行评审论文发表数量。(e) DETR在检测任务中重要发展的非详尽时间线概览。
<!-- BLOCK_END: b_027 -->

<!-- BLOCK: b_028 | type: paragraph | heading: Object Detection with Transformers: A Review > 1. Introduction -->
DN-DETR [35]使用加噪目标查询作为额外解码器输入，以减少DETR中二分匹配机制的不稳定性，该机制导致了收敛缓慢的问题。
AdaMixer [36]将编码器视为骨干网络和解码器之间的额外网络，由于其设计复杂性限制了性能并减缓了训练收敛。
它提出了一种三维采样过程和若干其他解码器修改。
REGO-DETR [37]提出了一种基于RoI的检测细化方法，以改善检测Transformer中的注意力机制。
DINO [38]考虑使用正负加噪目标查询使训练收敛更快，并增强小目标的检测性能。
在这些改进的基础上，Co-DETR [39]引入协作混合分配来提高训练稳定性和收敛速度，解决了二分匹配和小目标性能的局限性。
LW-DETR [40]关注效率，使用轻量级ViT编码器、浅层解码器和全局注意力来降低计算成本，同时保持具有竞争力的精度。
RT-DETR [41]结合混合编码器和多尺度特征处理以及IoU感知查询选择，实现自适应推理速度，在高精度和实时性能之间取得平衡。
快速的发展步伐使得系统性地追踪进展变得困难。
因此，对持续进展的综述是必要的，将有助于该领域的研究人员。
本文提供了检测Transformer近期进展的详细概述。
Table 1展示了检测Transformer（DETR）为提升性能和训练收敛所作的修改概览。
许多综述研究了目标检测中的深度学习方法[42–47]。
Table 2列出了现有的目标检测综述。
其中，多项研究全面综述了处理不同二维数据类型的方法[48–51]，而其他研究则关注特定二维应用[52–59]或相关任务，如分割[60–62]、图像描述[63–66]和目标跟踪[67]。
此外，一些综述考察了深度学习方法并介绍了视觉Transformer[68–71]。
尽管如此，这些综述大多发表于检测Transformer网络的近期改进之前，目前仍缺乏对基于Transformer的目标检测器的全面综述。
因此，有必要对持续进展进行详细综述，为研究人员提供指导和见解。
<!-- BLOCK_END: b_028 -->

<!-- BLOCK: b_030 | type: table_caption | heading: Object Detection with Transformers: A Review > 1. Introduction -->
Table 1。
检测Transformer（DETR）中加速训练收敛并提升小目标性能的改进概览。
其中，Bk代表骨干网络，Pre表示预训练，Attn表示注意力，Qry代表Transformer网络的查询。
每种方法代表对基线DETR的改进，绿色勾号表示引入修改的位置。
各网络的主要贡献总结在最后一列。
本表中所有GitHub链接均于2025年9月25日访问。
<!-- BLOCK_END: b_030 -->

<!-- BLOCK: b_031 | type: table | heading: Object Detection with Transformers: A Review > 1. Introduction -->
<table><tr><td rowspan="2">方法</td><td colspan="4">修改</td><td rowspan="2">发表</td><td rowspan="2">亮点</td></tr><tr><td>Bk</td><td>Pre</td><td></td><td>Attn Qry</td></tr><tr><td>DETR [11] GitHub https://github.com/facebookresearch/detr</td><td></td><td></td><td></td><td></td><td>ECCV 2020</td><td>Transformer，基于集合的预测，二分匹配</td></tr><tr><td>Deformable-DETR [20] GitHub https: //github.com/fundamentalvision/Deformable-DETR</td><td></td><td></td><td></td><td></td><td>ICLR 2021</td><td>可变形注意力模块</td></tr><tr><td>UP-DETR [21] GitHub https://github.com/dddzg/up-detr</td><td></td><td>5</td><td></td><td></td><td>CVPR 2021</td><td>无监督预训练，随机查询块检测</td></tr><tr><td>Efficient-DETR [22]</td><td></td><td></td><td></td><td></td><td>arXiv 2021</td><td>参考点和top-k查询选择模块</td></tr><tr><td>SMCA-DETR [23] GitHub https: //github.com/gaopengcuhk/SMCA-DETR</td><td></td><td></td><td></td><td></td><td>ICCV 2021</td><td>空间调制协同注意力模块</td></tr><tr><td>TSP-DETR [24] GitHub https: //github.com/Edward-Sun/TSP-Detection</td><td></td><td></td><td></td><td></td><td>ICCV 2021</td><td>用于交叉注意力的TSP-FCOS和TSP-RCNN模块</td></tr><tr><td>Conditional-DETR [25] GitHub htts: // github.com/Atten4Vis/ConditionalDETR</td><td></td><td></td><td></td><td></td><td>ICCV 2021</td><td>条件空间查询</td></tr><tr><td>WB-DETR [26] GitHub https://github.com/aybora/wbdetr</td><td>√</td><td></td><td></td><td></td><td>ICCV 2021</td><td>无骨干网络的编码器-解码器网络，LIE-T2T编码器模块</td></tr><tr><td>PnP-DETR [27] GitHub https: //github.com/twangnh/pnp-detr</td><td></td><td></td><td>√</td><td></td><td>ICCV 2021</td><td>PnP采样模块，包括池采样器和轮询采样器</td></tr><tr><td>Dynamic-DETR [28]</td><td></td><td></td><td></td><td></td><td>ICCV 2021</td><td>编码器-解码器网络中的动态注意力</td></tr><tr><td>YOLOS-DETR [29] GitHub https://github.com/hustvl/YOLOS</td><td></td><td></td><td></td><td></td><td>NeurIPS 2021</td><td>预训练编码器网络</td></tr><tr><td>Anchor-DETR [30] GitHub https: //github.com/megvii-research/AnchorDETR</td><td></td><td></td><td>√</td><td></td><td>AAAI 2022</td><td>行列解耦注意力，目标查询作为锚点</td></tr><tr><td>Sparse-DETR [31] GitHub https: //github.com/kakaobrain/sparse-detr D²ETR [32] GitHub https:</td><td></td><td></td><td></td><td></td><td>ICLR 2022</td><td>交叉注意力图预测器，可变形注意力模块</td></tr><tr><td>//github.com/alibaba/easyrobust/tree/main/ddetr</td><td></td><td></td><td>√</td><td></td><td>arXiv 2022</td><td>精细融合特征，跨尺度注意力模块</td></tr><tr><td>FP-DETR [33] GitHub https: //github.com/encounter1997/FP-DETR</td><td>√</td><td></td><td></td><td></td><td>ICLR 2022</td><td>多尺度令牌化替代CNN骨干网络，预训练编码器网络</td></tr><tr><td>CF-DETR [34]</td><td></td><td></td><td>√</td><td></td><td>AAAI 2022</td><td>TEF模块用于捕捉空间关系，解码器网络中的粗层和细层</td></tr><tr><td>DAB-DETR [72] GitHub https: // github.com/IDEA-Research/DAB-DETR</td><td></td><td></td><td></td><td></td><td>ICLR 2022</td><td>动态锚框作为目标查询</td></tr><tr><td>DN-DETR [35] GitHub https: //github.com/IDEA-Research/DN-DETR</td><td></td><td></td><td></td><td></td><td>CVPR 2022</td><td>正加噪目标查询</td></tr></table>
Table 1。
续。
<!-- BLOCK_END: b_031 -->

<!-- BLOCK: b_032 | type: table | heading: Object Detection with Transformers: A Review > 1. Introduction -->
<table><tr><td rowspan="2">方法</td><td colspan="4">修改</td><td rowspan="2">发表</td><td rowspan="2">亮点</td></tr><tr><td>Bk</td><td>Pre</td><td>Attn</td><td>Qry</td></tr><tr><td>AdaMixer [36] GitHub https: //github.com/MCG-NJU/AdaMixer</td><td></td><td></td><td></td><td></td><td>CVPR 2022</td><td>三维采样模块，解码器中的自适应混合模块</td></tr><tr><td>REGO [37] GitHub https: //github.com/zhechen/Deformable-DETR-REGO</td><td></td><td></td><td></td><td></td><td>CVPR 2022</td><td>多级循环机制和基于注视点的解码器</td></tr><tr><td>DINO [38] GitHub https: //github.com/facebookresearch/dino</td><td></td><td></td><td></td><td></td><td>arXiv 2022</td><td>对比去噪模块，正负加噪目标查询</td></tr><tr><td>Co-DETR [39] GitHub https: / / github.com/Sense-X/Co-DETR</td><td></td><td></td><td></td><td></td><td>ICCV 2023</td><td>协作混合分配实现更快收敛和更稳定的训练</td></tr><tr><td>LW-DETR [40] GitHub https: // github.com/Atten4Vis/LW-DETR</td><td></td><td></td><td></td><td></td><td>arXiv 2024</td><td>优化ViT编码器的轻量级DETR，浅层解码器及全局注意力</td></tr><tr><td>RT-DETR [41] GitHub https: //github.com/lyuwenyu/RT-DETR</td><td></td><td></td><td>√</td><td>√</td><td>CVPR 2024</td><td>多尺度特征混合编码器，IoU感知查询选择，自适应推理速度</td></tr></table>
<!-- BLOCK_END: b_032 -->

<!-- BLOCK: b_032a | type: table_caption | heading: Object Detection with Transformers: A Review > 1. Introduction -->
Table 2。
以往目标检测综述概览。
对于每篇论文，提供了发表详情。
<!-- BLOCK_END: b_032a -->

<!-- BLOCK: b_033 | type: table | heading: Object Detection with Transformers: A Review > 1. Introduction -->
<table><tr><td>标题</td><td>年份</td><td>发表场所</td><td>描述</td></tr><tr><td>Advanced Deep-Learning Techniques forSalient and Category-SpecificObject Detection: ASurvey[50]</td><td>2018</td><td>SPM</td><td>提供了不同目标检测领域的概述，包括目标检测（OD）、显著目标检测（SOD）和特定类别检测。</td></tr><tr><td>Object Detection in 20 Years: A Survey [73]</td><td>2019</td><td>TPAMI</td><td>本文概述了目标检测器的发展历程。</td></tr><tr><td>Deep Learning for Generic Object Detection: A Survey [51]</td><td>2019</td><td>IJCV</td><td>关于通用目标检测深度学习技术的综述。</td></tr><tr><td>A Survey on Deep Learning-based Architectures for Semantic Segmentationon2Dimages [53]</td><td>2020</td><td>PRJ</td><td>综述了基于深度学习的语义分割方法。</td></tr><tr><td>A Survey of Modern Deep Learning based Object Detection Models[74]</td><td>2021</td><td>ICV</td><td>简要概述了基于深度学习的（基于回归的单阶段和基于候选的两阶段）目标检测器。</td></tr><tr><td>A Survey of Object Detection Based on CNN and Transformer [70]</td><td>2021</td><td>PRML</td><td>综述了基于深度学习的目标检测器的优缺点，并介绍了基于Transformer的方法。</td></tr><tr><td>Transformers in computational visual media: A survey [71]</td><td>2021</td><td>CVM</td><td>关注使用视觉Transformer方法的骨干网络设计和底层视觉。</td></tr><tr><td>A survey: object detection methods from CNN to transformer [68]</td><td>2022</td><td>MTA</td><td>比较了各种基于CNN的检测网络，并介绍了基于Transformer的检测网络。</td></tr><tr><td>A Survey on Vision Transformer [69]</td><td>2023</td><td>TPAMI</td><td>本文提供了视觉Transformer的概述，并专注于总结视觉Transformer（ViT）领域的最先进研究。</td></tr></table>
<!-- BLOCK_END: b_033 -->

<!-- BLOCK: b_033a | type: list | heading: Object Detection with Transformers: A Review > 1. Introduction -->
1.
从架构角度对基于Transformer的检测方法进行详细综述。
我们根据骨干网络修改、预训练水平、注意力机制、查询设计等对检测Transformer（DETR）的改进进行分类和总结。该分析旨在帮助研究人员在性能指标方面对检测Transformer的关键组件形成更深入的理解。
2.
检测Transformer的性能评估。
我们使用流行的基准MS COCO [75]对检测Transformer的改进进行评估。
我们还强调了这些方法的优势和局限性。
3.
检测Transformer改进版本的精度与计算复杂度分析。
我们对最先进的基于Transformer的检测方法在注意力机制、骨干网络修改和查询设计方面进行了评估性比较。
4.
检测Transformer关键构建模块的概览，以进一步提升性能并展望未来方向。
我们考察了影响网络性能和训练收敛的各种关键架构设计模块的影响，为未来研究提供可能的建议。
对检测Transformer持续发展感兴趣的读者可以参考我们的GitHub仓库：https://github.com/mindgarage-shan/transformer\_object\_detection\_survey（访问日期：2025年9月25日）。
<!-- BLOCK_END: b_033a -->

<!-- BLOCK: b_033b | type: paragraph | heading: Object Detection with Transformers: A Review > 1. Introduction -->
本文其余部分安排如下。
第2节涉及目标检测和Transformer在各类视觉中的应用。
第3节是主要部分，详细阐述了检测Transformer中的修改。
Section 3.24涉及评估协议，第4节提供了检测Transformer的比较评估。
第5节讨论了开放性挑战和未来方向。
最后，第6节总结了全文。
<!-- BLOCK_END: b_033b -->

<!-- BLOCK: b_034 | type: heading | heading: Object Detection with Transformers: A Review > 2. Object Detection and Transformers in Vision -->
## 2.
视觉中的目标检测与Transformers
<!-- BLOCK_END: b_034 -->

<!-- BLOCK: b_035 | type: heading | heading: Object Detection with Transformers: A Review > 2.1. Object Detection -->
## 2.1.
目标检测
<!-- BLOCK_END: b_035 -->

<!-- BLOCK: b_036 | type: paragraph | heading: Object Detection with Transformers: A Review > 2.1. Object Detection -->
本节阐述目标检测的关键概念及以往使用的目标检测器。
关于目标检测概念的更详细分析可参见[74,76,77]。
目标检测任务通过提供每个目标周围的边界框及其类别来定位和识别图像中的目标。
这些检测器通常在PASCAL VOC [78]或MS COCO [75]等数据集上进行训练。
骨干网络将输入图像的特征提取为特征图[79]。
通常，骨干网络（如ResNet-50 [80]）在ImageNet [81]上进行预训练，然后微调至下游任务[82–87]。
此外，许多工作也使用视觉Transformer[3,88,89]作为骨干网络。
单阶段目标检测器[3,4,90–98]仅使用一个网络，速度更快但性能低于两阶段网络。
两阶段目标检测器[1,2,7,79,99–104]包含两个网络，分别提供最终的边界框和类别标签。
轻量级检测器：轻量级检测器旨在比标准目标检测模型具有更高的计算效率。
这些是实时目标检测器，可部署在小型设备上。
例如[105–114]。
三维目标检测：三维目标检测的主要目的是使用三维边界框识别感兴趣的目标并给出类别标签。
三维方法分为三类：基于图像的[115–121]、基于点云的[122–130]和多模态融合[131–135]。
<!-- BLOCK_END: b_036 -->

<!-- BLOCK: b_039 | type: heading | heading: Object Detection with Transformers: A Review > 2.2. Transformer for Segmentation -->
## 2.2.
用于分割的Transformer
<!-- BLOCK_END: b_039 -->

<!-- BLOCK: b_040 | type: paragraph | heading: Object Detection with Transformers: A Review > 2.2. Transformer for Segmentation -->
自注意力机制可用于分割任务[136–140]，提供像素级[141]预测结果。
全景分割[142]通过提供逐像素的类别和实例标签，联合解决语义分割和实例分割任务。
Wang等人[143]提出了位置敏感轴向注意力，用于三个基准[75,144,145]上的全景分割任务。
上述分割方法在基于CNN的网络中具有自注意力。
近期，包含编码器-解码器模块的分割Transformer[137,139]为将Transformer应用于分割任务提供了新方向。
<!-- BLOCK_END: b_040 -->

<!-- BLOCK: b_041 | type: heading | heading: Object Detection with Transformers: A Review > 2.3. Transformers for Scene and Image Generation -->
## 2.3.
用于场景和图像生成的Transformers
<!-- BLOCK_END: b_041 -->

<!-- BLOCK: b_042 | type: paragraph | heading: Object Detection with Transformers: A Review > 2.3. Transformers for Scene and Image Generation -->
以往，文本到图像生成方法[146–149]基于GAN[150]。
Ramesh等人[151]引入了一种基于Transformer的模型，用于从提供的文本描述生成高质量图像。
Transformer网络也应用于图像合成[152–156]，这对学习无监督和生成模型用于下游任务非常重要。
使用无监督训练程序[153]的特征学习在两个数据集[157,158]上达到了最先进的性能，而SimCLR [159]在[160]上提供了可比较的性能。
iGPT图像生成网络[153]不包含类似于语言建模任务的预训练程序。
然而，无监督的基于CNN的网络[161–163]将先验知识作为架构布局、注意力机制和正则化。
具有基于CNN骨干网络的生成对抗网络（GAN）[150]在图像合成[164–166]方面具有吸引力。
TransGAN [155]是一个强大的GAN网络，其中生成器和判别器包含Transformer模块。
这些基于Transformer的网络提升了场景和图像生成任务的性能。
<!-- BLOCK_END: b_042 -->

<!-- BLOCK: b_043 | type: heading | heading: Object Detection with Transformers: A Review > 2.4. Transformers for Low-Level Vision -->
## 2.4.
用于底层视觉的Transformers
<!-- BLOCK_END: b_043 -->

<!-- BLOCK: b_044 | type: paragraph | heading: Object Detection with Transformers: A Review > 2.4. Transformers for Low-Level Vision -->
底层视觉分析图像以识别其基本组件，并为进一步处理和更高级任务创建中间表示。
在观察到注意力网络在高级视觉任务中的卓越表现[11,137]后，许多基于注意力的方法被引入以解决底层视觉问题，如[167–171]。
<!-- BLOCK_END: b_044 -->

<!-- BLOCK: b_045 | type: heading | heading: Object Detection with Transformers: A Review > 2.5. Transformers for Multi-Modal Tasks -->
## 2.5.
用于多模态任务的Transformers
<!-- BLOCK_END: b_045 -->

<!-- BLOCK: b_046 | type: paragraph | heading: Object Detection with Transformers: A Review > 2.5. Transformers for Multi-Modal Tasks -->
多模态任务涉及处理和整合来自多个信息源或模态的信息，如文本、图像、音频或视频。
Transformer网络在视觉语言任务中的应用也已广泛展开，包括视觉问答[172]、视觉常识推理[173]、跨模态检索[174]和图像描述[175]。
这些Transformer设计可分为单流[176–181]和双流网络[182–184]。
这些网络之间的主要区别在于损失函数的选择。
<!-- BLOCK_END: b_046 -->

<!-- BLOCK: b_047 | type: heading | heading: Object Detection with Transformers: A Review > 3. Detection Transformers -->
## 3.
检测Transformers
<!-- BLOCK_END: b_047 -->

<!-- BLOCK: b_048 | type: paragraph | heading: Object Detection with Transformers: A Review > 3. Detection Transformers -->
本节简要介绍检测Transformer（DETR）及其改进，如Figure 2所示。
<!-- BLOCK_END: b_048 -->

<!-- BLOCK: b_049 | type: figure_caption | heading: Object Detection with Transformers: A Review > 3. Detection Transformers -->
![](Images_GFP684MN/3ad96e0c4515515e204e359b1fbc5d84d5b9417f98b92b2880b6f417fbbf0d4c.jpg) Figure 2。
检测Transformer（DETR）及其近期方法为提升性能和训练收敛所提出的修改概览。
它将检测视为集合预测任务，并使用Transformer使网络摆脱非极大值抑制（NMS）等后处理步骤。
其中，添加到DETR的每个模块以不同颜色表示，并标注对应标签（显示在右侧）。
<!-- BLOCK_END: b_049 -->

<!-- BLOCK: b_050 | type: heading | heading: Object Detection with Transformers: A Review > 3.1. DETR -->
## 3.1.
DETR
<!-- BLOCK_END: b_050 -->

<!-- BLOCK: b_051 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.1. DETR -->
检测Transformer（DETR）[11]的架构比基于CNN的检测器（如faster R-CNN [185]）简洁得多，因为它无需锚点生成过程和非极大值抑制（NMS）等后处理步骤，并提供了一个最优的检测框架。
DETR网络包含三个主要模块：带有位置编码的骨干网络、编码器和带有注意力机制的解码器网络。
从骨干网络提取的特征是一个向量及其位置编码[186,187]，作为输入向量送入编码器网络。
在此过程中，对转发到多头注意力和前馈网络的键、查询和值矩阵执行自注意力操作，以求得输入向量的注意力概率。
DETR解码器将目标查询与编码器输出并行处理。
它通过并行解码N个目标查询来计算预测结果。
它采用二分匹配算法来标记真实标注和预测对象，如以下公式所示：
<!-- BLOCK_END: b_051 -->

<!-- BLOCK: b_052 | type: equation | heading: Object Detection with Transformers: A Review > 3.1. DETR -->
$$
\hat { \sigma } = \arg \operatorname* { m i n } _ { \sigma \in N } \sum _ { k } ^ { N } \mathcal { L } _ { m } ( y _ { k } , \hat { y } _ { \sigma ( k ) } ) .\tag{1}
$$
<!-- BLOCK_END: b_052 -->

<!-- BLOCK: b_053 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.1. DETR -->
其中，$y _ { k }$是真实标注（GT）对象的集合。
它为"有对象"和"无对象"两类均提供边界框，其中N是待检测对象的总数。
$\mathcal { L } _ { m } \big ( y _ { k } , \hat { y } _ { \sigma ( k ) } \big )$表示预测对象$\sigma ( k )$与真实标注$y _ { k } ,$之间的无重复匹配代价，定义如下：
<!-- BLOCK_END: b_053 -->

<!-- BLOCK: b_054 | type: equation | heading: Object Detection with Transformers: A Review > 3.1. DETR -->
$$
\mathcal { L } _ { m } ( y _ { k } , \hat { y } _ { \sigma ( k ) } ) = - \mathbb { 1 } _ { \{ c _ { k } \neq \phi \} } \hat { p } _ { \sigma ( k ) } ( c _ { k } ) + \mathbb { 1 } _ { \{ c _ { k } \neq \phi \} } \mathcal { L } _ { b b o x } ( b _ { k } , \hat { b } _ { \hat { \sigma } } ( k ) ) .\tag{2}
$$
<!-- BLOCK_END: b_054 -->

<!-- BLOCK: b_055 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.1. DETR -->
下一步是通过确定真实标注（GT）与检测框在边界框区域和标签方面的最优匹配来计算匈牙利损失。
该损失通过随机梯度下降（SGD）来最小化。
<!-- BLOCK_END: b_055 -->

<!-- BLOCK: b_056 | type: equation | heading: Object Detection with Transformers: A Review > 3.1. DETR -->
$$
\begin{array} { r } { \mathcal { L } _ { H } ( y , \hat { y } ) = \sum _ { k = 1 } ^ { N } [ - l o g \hat { p } _ { \hat { \sigma } ( k ) } ( c _ { k } ) + \mathbb { 1 } _ { \{ c _ { k } \neq \phi \} } \mathcal { L } _ { b o x } ( b _ { k } , \hat { b } _ { \hat { \sigma } } ( k ) ) ] , } \end{array}\tag{3}
$$
<!-- BLOCK_END: b_056 -->

<!-- BLOCK: b_057 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.1. DETR -->
其中，$\hat { p } _ { \hat { \sigma } ( k ) }$和$c _ { k }$分别为预测类别和目标标签。
其中$\hat { \sigma }$是最优分配因子；$b _ { k }$和$\hat { b } _ { \hat { \sigma } } ( \boldsymbol { k } )$分别是真实标注和预测的边界框。
ŷ和$y = \{ ( c _ { k } , b _ { k } ) \}$分别为对象的预测值和真实标注。
具体而言，边界框损失是广义IoU（GIoU）损失[188]与L1损失的线性组合，如以下公式所示：
<!-- BLOCK_END: b_057 -->

<!-- BLOCK: b_058 | type: equation | heading: Object Detection with Transformers: A Review > 3.1. DETR -->
$$
\mathcal { L } _ { b b o x } = \lambda _ { i } \mathcal { L } _ { i o u } ( b _ { k } , \hat { b } _ { \sigma ( k ) } ) + \lambda _ { l 1 } \parallel b _ { k } - \hat { b } _ { \sigma ( k ) } \parallel _ { 1 } ,\tag{4}
$$
<!-- BLOCK_END: b_058 -->

<!-- BLOCK: b_059 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.1. DETR -->
其中，$\lambda _ { i }$和$\lambda _ { l 1 }$为超参数。
DETR在单次推理中只能预测固定数量N个对象。
对于COCO数据集[75]，N的值设为100，因为该数据集有80个类别。
该网络无需NMS来去除冗余预测，因为它采用二分匹配损失和并行解码[189–191]。
相比之下，先前的研究采用了基于RNN的自回归解码[192–194,194–196]。
DETR网络面临若干挑战，如训练收敛缓慢和小目标性能下降。
为了应对这些挑战，研究者们对DETR网络进行了改进。
尽管采用端到端设计，DETR仍存在训练收敛缓慢和小目标精度较低的问题。
均匀的注意力初始化以及缺乏多尺度特征使得精确学习目标位置变得困难。
这些局限性推动了多项改进方法的发展，旨在提升收敛速度、计算效率和小目标检测性能。
<!-- BLOCK_END: b_059 -->

<!-- BLOCK: b_060 | type: heading | heading: Object Detection with Transformers: A Review > 3.2. Deformable-DETR -->
## 3.2.
Deformable-DETR
<!-- BLOCK_END: b_060 -->

<!-- BLOCK: b_061 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.2. Deformable-DETR -->
DETR的注意力模块在初始化阶段为输入特征图的所有像素赋予均匀的权重值。
这些权重需要多个训练轮次才能收敛，从而找到具有信息量的像素位置。
然而，这需要大量的计算和广泛的内存。
编码器的自注意力复杂度为$O ( w _ { i } ^ { 2 } h _ { i } ^ { 2 } c _ { i } )$。
相比之下，解码器的交叉注意力复杂度为$O ( h _ { i } w _ { i } c _ { i } ^ { 2 } + N h _ { i } w _ { i } c _ { i } )$。
形式上，$h _ { i }$和$w _ { i }$分别表示输入特征图的高度和宽度，N表示作为输入馈送到解码器的目标查询。
设$q \in \Omega _ { q }$表示具有特征$z _ { q } \in R ^ { c _ { i } }$的查询元素，$k \in \Omega _ { k }$表示具有特征$\boldsymbol { x } _ { k } \in R ^ { c _ { i } } ,$的键向量，其中$c _ { i }$是输入特征维度，$\Omega _ { k }$和$\Omega _ { q }$分别表示键向量集合和查询向量集合。
然后，多头注意力（MHAttn）的特征按以下方式计算：
<!-- BLOCK_END: b_061 -->

<!-- BLOCK: b_062 | type: equation | heading: Object Detection with Transformers: A Review > 3.2. Deformable-DETR -->
$$
\begin{array} { r } { M H A t t n ( z _ { q } , x ) = \sum _ { j = 1 } ^ { J } W _ { j } [ \sum _ { k \in \Omega _ { k } } A _ { j q k } . W _ { j } ^ { \prime } x _ { k } ] , } \end{array}\tag{5}
$$
<!-- BLOCK_END: b_062 -->

<!-- BLOCK: b_063 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.2. Deformable-DETR -->
其中j表示注意力头，$W _ { j } \in \mathbb { R } ^ { c _ { i } \times c _ { v } } .$，$W _ { j } ^ { \prime } \in \mathbb { R } ^ { c _ { v } \times c _ { i } }$为默认可学习权重$( c _ { v } = c _ { i } / J$）。
注意力权重$A _ { j q k }$ ∝ ex $\gamma \frac { z _ { q } ^ { T } U _ { j } ^ { T } V _ { j } x _ { k } } { \sqrt { c } _ { v } }$被归一化为$\begin{array} { r } { \sum _ { k \in \Omega _ { k } } A _ { j q k } = 1 } \end{array}$，其中$U _ { j } , V _ { j } \in R ^ { c _ { v } \times c _ { i } }$也是可学习的权重。
Deformable-DETR [20]受[197,198]启发修改了注意力模块，以处理图像特征图，其出发点是将注意力网络视为训练收敛缓慢和特征空间分辨率受限的主要原因。
该模块在每个参考点附近采样一小部分特征。
给定输入特征图$x \in R ^ { c _ { i } \times h _ { i } \times w _ { i } }$，设查询q具有内容特征$z _ { q }$和二维参考点$\boldsymbol { r } _ { q } ,$，则可变形注意力特征按以下方式计算：
<!-- BLOCK_END: b_063 -->

<!-- BLOCK: b_064 | type: equation | heading: Object Detection with Transformers: A Review > 3.2. Deformable-DETR -->
$$
\begin{array} { r } { D e f o r m A t t n ( z _ { q } , r _ { q } , x ) = \sum _ { j = 1 } ^ { J } W _ { j } [ \sum _ { k = 1 } ^ { K } A _ { j q k } . W _ { j } x ( r _ { q } + \Delta r _ { j q k } ) ] , } \end{array}\tag{6}
$$
<!-- BLOCK_END: b_064 -->

<!-- BLOCK: b_065 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.2. Deformable-DETR -->
其中$\Delta r _ { j q k }$索引采样偏移。
它所需的训练轮次仅为简单DETR网络的十分之一。
自注意力的复杂度变为$O ( w _ { i } h _ { i } c _ { i } ^ { 2 } )$，相对于空间尺寸$h _ { i } w _ { i }$呈线性复杂度。
解码器中交叉注意力的复杂度变为$O ( N K c _ { i } ^ { 2 } )$，与空间尺寸$h _ { i } w _ { i }$无关。
在图$^ { 3 , }$中，深粉色方块表示Deformable-DETR中的可变形注意力模块。
<!-- BLOCK_END: b_065 -->

<!-- BLOCK: b_066 | type: figure_caption | heading: Object Detection with Transformers: A Review > 3.2. Deformable-DETR -->
![](Images_GFP684MN/cab0f6b4d2cd79ad867c59e82f845c212ae20f0e6690b6a3d6342d7f10153a41.jpg) Figure 3.
在加入Deformable-DETR [20]、UP-DETR [21]和Efficient-DETR [22]之后原始DETR的结构。
此处，网络为简单的DETR网络，改进部分由小色块标示。
深粉色方块表示Deformable-DETR，亮青色方块表示UP-DETR，暗绿色方块表示Efficient-DETR。
<!-- BLOCK_END: b_066 -->

<!-- BLOCK: b_067 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.2. Deformable-DETR -->
多尺度特征图：高分辨率输入图像特征提升了网络效率，尤其对小目标而言。
然而，这在计算上是昂贵的。
Deformable-DETR在不影响计算量的前提下提供高分辨率特征。
它采用包含高低分辨率特征的特征金字塔，而非原始的高分辨率输入图像特征图。
该特征金字塔的输入图像分辨率为$1 / 8 , 1 / 1 6 ,$和1/32，并包含其相对位置嵌入。
此外，Deformable-DETR将DETR中的注意力模块替换为多尺度可变形注意力模块，以降低计算复杂度并提升性能。
虽然Deformable-DETR加速了训练并改善了小目标检测，但设计有效的采样偏移和管理多尺度特征交互仍然是实现最优性能的关键。
算法1展示了多尺度可变形注意力机制的逐步实现过程，补充了前述的数学公式。
算法1：Deformable-DETR中的多尺度可变形注意力。
输入：特征图$\overline { { \mathcal { F } = \left\{ F _ { 1 } , F _ { 2 } , \ldots \right\} } }$，查询特征$Q ,$ 参考点$R ,$ 采样偏移$\Delta r$ 输出：更新后的查询特征$Q ^ { \prime }$ 1 对每个查询$q \in Q$执行 2 初始化注意力结果$z 0 ;$ 3 对每个注意力头$j = 1 t o J$执行 4 对每个采样点$k = 1$到K执行 5 计算采样位置：$p r [ q ] + \Delta r [ j , k ] ;$ 6 插值特征：$x \gets$ 采样特征$( \mathcal { F } , p ) ;$ 7 更新注意力：$z z + A [ j , q , k ] \cdot W _ { j } \cdot x ;$ 8 跨注意力头聚合z并更新$q ;$ 9 返回$Q ^ { \prime }$
<!-- BLOCK_END: b_067 -->

<!-- BLOCK: b_069 | type: heading | heading: Object Detection with Transformers: A Review > 3.3. UP-DETR -->
## 3.3.
UP-DETR
<!-- BLOCK_END: b_069 -->

<!-- BLOCK: b_070 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.3. UP-DETR -->
Dai等人[21]提出了一些改进方法，以类似于NLP中Transformer预训练的方式对DETR进行预训练。
从输入图像中随机裁剪的图像块被用作解码器的目标查询输入。
UP-DETR提出的预训练方法有助于检测这些随机尺寸的查询图像块。
算法2总结了UP-DETR的预训练过程，展示了如何通过随机图像块、查询分组和注意力掩码来改善收敛和特征学习。
在Figure 3中，亮青色方块表示UP-DETR。
预训练过程中解决了两个问题：多任务学习和多查询定位。
多任务学习：目标检测任务结合了目标定位和分类，而这些任务通常具有不同的特征[199–201]。
图像块检测会损害分类特征。
提出了使用图像块特征重建和冻结预训练骨干网络的多任务学习方法，以保护Transformer的分类特征。
特征重建如下：
<!-- BLOCK_END: b_070 -->

<!-- BLOCK: b_072 | type: equation | heading: Object Detection with Transformers: A Review > 3.3. UP-DETR -->
$$
\mathcal { L } _ { r e c } ( f _ { k } , \hat { f } _ { \hat { \sigma } ( k ) } ) = \parallel \frac { f _ { k } } { \parallel f _ { k } \parallel _ { 2 } } - \frac { \hat { f } _ { \hat { \sigma } ( k ) } } { \parallel \hat { f } _ { \hat { \sigma } ( k ) } \parallel _ { 2 } } \parallel _ { 2 } ^ { 2 } .\tag{7}
$$
<!-- BLOCK_END: b_072 -->

<!-- BLOCK: b_073 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.3. UP-DETR -->
其中，特征重建项为$\mathcal { L } _ { r e c }$。
它是从CNN骨干网络获得的图像块的l2（归一化）特征之间的均方误差。
多查询定位：DETR的解码器以目标查询作为输入，以关注不同的位置和边界框尺寸。
当目标查询数量N较大（通常N = 100）时，单一查询组不合适，因为存在收敛问题。
为解决目标查询与图像块之间的多查询定位问题，UP-DETR提出了一种注意力掩码和查询打乱机制。
目标查询的数量被分为X个不同的组，每个图像块被分配给N/X个目标查询。
解码器中自注意力模块的Softmax层通过添加受[202]启发的注意力掩码进行修改，如下所示：
<!-- BLOCK_END: b_073 -->

<!-- BLOCK: b_075 | type: equation | heading: Object Detection with Transformers: A Review > 3.3. UP-DETR -->
$$
P ( q _ { i } , k _ { i } ) = S o f t m a x ( \frac { q _ { i } k _ { i } ^ { T } } { \sqrt { d } } + M ) v _ { i } ,\tag{8}
$$
<!-- BLOCK_END: b_075 -->

<!-- BLOCK: b_076 | type: equation | heading: Object Detection with Transformers: A Review > 3.3. UP-DETR -->
$$
M _ { k , l } = \left\{ \begin{array} { l l } { { 0 } } & { { \ k , l \ i n \ t h e \ s a m e \ g r o u p } } \\ { { - \infty } } & { { \ o t h e r w i s e } } \end{array} \right. ,\tag{9}
$$
<!-- BLOCK_END: b_076 -->

<!-- BLOCK: b_077 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.3. UP-DETR -->
其中$M _ { k , l }$是目标查询$q _ { k }$和$q _ { l }$的交互参数。
尽管目标查询被分为不同的组，但在下游训练任务中这些查询没有显式的分组。
因此，在预训练期间通过类似dropout [203]的方式将10%个查询图像块遮蔽为零来对这些查询进行随机打乱。
虽然UP-DETR改善了收敛和查询学习，但预训练可能无法完美迁移到下游检测任务，其分组和遮蔽机制需要仔细调优以避免收敛或性能问题。
算法2展示了图像块检测预训练过程，其中裁剪随机图像块，将其分配到具有注意力掩码的查询子集，训练模型预测图像块位置同时重建特征，从而提高鲁棒性和收敛性。
算法2：UP-DETR中的图像块检测预训练。
输入：输入图像I，随机图像块集$P ,$ 目标查询Q 输出：预训练的DETR模型 1 从I中随机裁剪图像块形成$P ;$ 2 使用冻结的骨干网络提取图像特征；3 对每个图像块$p \in P$执行 4 将p分配到查询子集$Q _ { g } \subset Q ;$ 5 应用注意力掩码将注意力限制在$Q _ { g } ;$内 6 解码器预测图像块位置和尺寸；7 计算定位损失$\mathcal { L } _ { l o c }$和特征重建损失$\mathcal { L } _ { r e c } { ; }$ 8 打乱查询分配并遮蔽10%个查询（dropout风格）；9 反向传播并更新模型参数。
<!-- BLOCK_END: b_077 -->

<!-- BLOCK: b_079 | type: heading | heading: Object Detection with Transformers: A Review > 3.4. Efficient-DETR -->
## 3.4.
Efficient-DETR
<!-- BLOCK_END: b_079 -->

<!-- BLOCK: b_080 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.4. Efficient-DETR -->
DETR的性能也取决于目标查询，因为检测头从它们那里获得最终预测。
然而，这些目标查询在训练开始时是随机初始化的。
Efficient-DETR [22]基于DETR和Deformable-DETR，研究了随机初始化的目标块，包括参考点和目标查询，这是需要多次训练迭代的原因之一。
在Figure 3中，暗绿色方块表示Efficient-DETR。
Efficient-DETR有两个主要模块：密集模块和稀疏模块。
这些模块共享相同的最终检测头。
密集模块包括骨干网络、编码器网络和检测头。
遵循[204]，它通过使用滑动窗口的类别特定密集预测生成候选区域，并选择Top-k特征作为目标查询和参考点。
Efficient-DETR使用四维边界框作为参考点，而非二维中心点。
稀疏网络执行与密集网络相同的工作，只是输出尺寸不同。
密集模块的特征被用作稀疏模块的初始状态，这被认为是目标查询的良好初始化。
密集模块和稀疏模块都使用一对一分配规则，如[205–207]中所述。
然而，Efficient-DETR增加了架构复杂性，最终性能在很大程度上取决于密集模块候选区域的质量，使得该方法对初始目标查询和超参数的选择敏感。
<!-- BLOCK_END: b_080 -->

<!-- BLOCK: b_082 | type: heading | heading: Object Detection with Transformers: A Review > 3.5. SMCA-DETR -->
## 3.5.
SMCA-DETR
<!-- BLOCK_END: b_082 -->

<!-- BLOCK: b_083 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.5. SMCA-DETR -->
DETR的解码器以目标查询作为输入，负责在不同空间位置进行目标检测。
这些目标查询与来自编码器的空间特征相结合。
DETR中的协同注意力机制涉及计算目标查询与图像特征之间的一组注意力图，以提供类别标签和边界框位置。
然而，DETR解码器中与目标查询相关的视觉区域可能与预测的边界框无关。
这是DETR需要多个训练轮次才能找到合适的视觉位置以正确识别对应对象的原因之一。
Gao等人[23]引入了空间调制协同注意力（SMCA）模块，替换DETR中现有的协同注意力机制，以克服DETR训练收敛缓慢的问题。
在Figure 4中，紫色方块表示SMCA-DETR。
目标查询估计其对应对象的尺度和中心，这些进一步用于建立二维空间权重图。
目标查询q的高斯类分布的尺度$l _ { h _ { i } } , l _ { w _ { i } }$和中心$e _ { h _ { i } } , e _ { w _ { i } }$的初始估计如下：
<!-- BLOCK_END: b_083 -->

<!-- BLOCK: b_084 | type: equation | heading: Object Detection with Transformers: A Review > 3.5. SMCA-DETR -->
$$
e _ { h _ { i } } ^ { n r m } , e _ { w _ { i } } ^ { n r m } = s i g m o i d ( M L P ( q ) ) ,\tag{10}
$$
<!-- BLOCK_END: b_084 -->

<!-- BLOCK: b_085 | type: equation | heading: Object Detection with Transformers: A Review > 3.5. SMCA-DETR -->
$$
l _ { h _ { i } } , l _ { w _ { i } } = F C ( q ) ,\tag{11}
$$
<!-- BLOCK_END: b_085 -->

<!-- BLOCK: b_086 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.5. SMCA-DETR -->
其中目标查询q在经过两层MLP后通过Sigmoid激活函数以归一化形式提供预测中心。
这些预测中心被反归一化以获得输入图像的中心坐标$e _ { h _ { i } }$和$e _ { w _ { i } }$。
目标查询还将对象尺度估计为$l _ { h _ { i } }$和$l _ { w _ { i } }$。
在预测对象尺度和中心之后，SMCA提供如下高斯类权重图：
<!-- BLOCK_END: b_086 -->

<!-- BLOCK: b_087 | type: equation | heading: Object Detection with Transformers: A Review > 3.5. SMCA-DETR -->
$$
\mathbf { W } ( x , y ) = e x p \left( - \frac { ( x - e _ { w _ { i } } ) ^ { 2 } } { \beta l _ { w _ { i } } ^ { 2 } } - \frac { ( y - e _ { h _ { i } } ) ^ { 2 } } { \beta l _ { h _ { i } } ^ { 2 } } \right) ,\tag{12}
$$
<!-- BLOCK_END: b_087 -->

<!-- BLOCK: b_088 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.5. SMCA-DETR -->
其中$\beta$是调节带宽的超参数，$( x , y )$是权重图W的空间参数。它对靠近中心的空间位置赋予高注意力，对远离中心的空间位置赋予低注意力。
<!-- BLOCK_END: b_088 -->

<!-- BLOCK: b_089 | type: equation | heading: Object Detection with Transformers: A Review > 3.5. SMCA-DETR -->
$$
A _ { i } = S o f t m a x ( \frac { q _ { i } k _ { i } ^ { T } } { \sqrt { d } } + \mathbf { l o g } \mathbf { W } ) v _ { i } .\tag{13}
$$
<!-- BLOCK_END: b_089 -->

<!-- BLOCK: b_090 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.5. SMCA-DETR -->
其中，$A _ { i }$是协同注意力图。
DETR中的协同注意力模块与该协同注意力模块的区别在于加入了空间图W的对数。解码器注意力网络在预测框区域附近分配更多注意力，这限制了搜索位置，从而使网络更快收敛。
SMCA-DETR提升了训练效率和小目标检测性能。
然而，其成功取决于对象中心和尺度的准确初始预测，使其对初始化和超参数敏感。
<!-- BLOCK_END: b_090 -->

<!-- BLOCK: b_091 | type: figure_caption | heading: Object Detection with Transformers: A Review > 3.5. SMCA-DETR -->
![](Images_GFP684MN/10f0a4be4a6623af75fb24fa5bf28e393d63f648d4771a9cffaeb0e05ce5ba00.jpg) Figure 4.
在加入SMCA-DETR [23]、TSP-DETR [24]和Conditional-DETR [25]之后原始DETR的结构。
此处，网络为简单的DETR网络，改进部分由小色块标示。
紫色方块表示SMCA-DETR，橙色方块表示TSP-DETR，黄色方块表示Conditional-DETR。
<!-- BLOCK_END: b_091 -->

<!-- BLOCK: b_092 | type: heading | heading: Object Detection with Transformers: A Review > 3.6. TSP-DETR -->
## 3.6.
TSP-DETR
<!-- BLOCK_END: b_092 -->

<!-- BLOCK: b_093 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.6. TSP-DETR -->
TSP-DETR [24]处理交叉注意力和二分匹配的不稳定性，以克服DETR训练收敛缓慢的问题。
TSP-DETR提出了两个基于编码器网络和特征金字塔网络（FPN）[79]的模块，以加速DETR的训练收敛。
在Figure 4中，橙色方块表示TSP-DETR。
这些模块是TSP-FCOS和TSP-RCNN，分别使用经典的单阶段检测器FCOS [208]和经典的两阶段检测器Faster-RCNN [1]。
TSP-FCOS使用了新的感兴趣特征（FoI）模块来处理Transformer编码器中的多层特征。
两个模块都使用二分匹配机制来加速训练收敛。
TSP-FCOS：TP-FCOS模块遵循FCOS [208]来设计骨干网络和FPN [79]。
首先，由CNN骨干网络从输入图像中提取的特征被送入FPN组件以产生多层级特征。
两个特征提取头——分类头和辅助头——使用四个卷积层和组归一化[209]，这些在特征金字塔各层级间共享。
然后，FoI分类器对这些头的拼接输出进行过滤，以选择得分最高的特征。
最后，Transformer编码器网络将这些感兴趣特征（FoI）及其位置编码作为输入，输出类别标签和边界框。
TSP-RCNN：与TP-FCOS类似，该模块从CNN骨干网络提取特征，并使用FPN组件产生多层级特征。
与TSP-FCOS中使用的两个特征提取头不同，TSP-RCNN模块遵循faster R-CNN [1]的设计。
它使用区域提议网络（RPN）来寻找需要进一步细化的感兴趣区域（RoI）。
该模块中的每个RoI都具有一个对象性得分以及一个预测边界框。
RoIAlign [101]应用于多层级特征图以获取RoI信息。
在经过全连接网络后，这些提取的特征被送入Transformer编码器作为输入。
这些RoI候选区域的位置信息为四个值$\left( { { c _ { n x } } , { c _ { n y } } , { w _ { n } } , { h _ { n } } } \right)$，其中$( c _ { n x } , c _ { n y } ) \in [ 0 , 1 ] ^ { 2 }$表示中心的归一化值，$( w _ { n } , h _ { n } ) \in [ 0 , 1 ] ^ { 2 }$表示高度和宽度的归一化值。
最后，Transformer编码器网络将这些感兴趣区域（RoI）及其位置编码作为输入，以进行精确预测。
TSP-DETR中的FCOS和RCNN模块加速了训练收敛并提升了DETR网络的性能。
<!-- BLOCK_END: b_093 -->

<!-- BLOCK: b_096 | type: heading | heading: Object Detection with Transformers: A Review > 3.7. Conditional-DETR -->
## 3.7.
Conditional-DETR
<!-- BLOCK_END: b_096 -->

<!-- BLOCK: b_097 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.7. Conditional-DETR -->
DETR网络中的交叉注意力模块需要高质量的输入嵌入来预测准确的边界框和类别标签。
高质量的内容嵌入增加了训练收敛的难度。
Conditional-DETR [25]提出了一种条件交叉注意力机制来解决DETR的训练收敛问题。
它与简单的DETR的区别在于交叉注意力的输入键$k _ { i }$和输入查询$q _ { i }$。
在Figure 4中，黄色方块表示Conditional-DETR。
条件查询从二维坐标以及前一个解码器层的嵌入输出中获得。
从解码器嵌入预测的候选框如下：
<!-- BLOCK_END: b_097 -->

<!-- BLOCK: b_098 | type: equation | heading: Object Detection with Transformers: A Review > 3.7. Conditional-DETR -->
$$
b o x = s i g ( F F N ( e ) + [ r ^ { T } 0 0 ] ^ { T } ) .\tag{14}
$$
<!-- BLOCK_END: b_098 -->

<!-- BLOCK: b_099 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.7. Conditional-DETR -->
其中，e是作为输入馈送到解码器的输入嵌入。
该框是一个四维向量$[ b o x _ { c x } b o x _ { c y } b o x _ { w } b o x _ { h } ] .$，其中框中心值为$\left( b o x _ { c x } , b o x _ { c y } \right)$，宽度值为box${ \bf \dot { \theta } } _ { w } ,$，高度值为boxh。
$s i g ( )$函数对预测值进行归一化，取值范围为0到1。
FFN()预测未归一化的边界框。r是参考点的未归一化二维坐标，(0, 0)对应简单的DETR。
该工作要么为每个边界框学习参考点r，要么从相应的目标查询生成它。
它从解码器的输入嵌入中学习多头交叉注意力的查询。
这种空间查询使交叉注意力头考虑显式区域，通过缩小空间范围来帮助定位类别标签和边界框的不同区域。
<!-- BLOCK_END: b_099 -->

<!-- BLOCK: b_100 | type: heading | heading: Object Detection with Transformers: A Review > 3.8. WB-DETR -->
## 3.8.
WB-DETR
<!-- BLOCK_END: b_100 -->

<!-- BLOCK: b_101 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.8. WB-DETR -->
DETR使用CNN骨干网络提取局部特征，并通过Transformer的编码器-解码器网络获取全局上下文。
WB-DETR [26]证明了在检测Transformer中使用CNN骨干网络进行特征提取并非必需。
它包含一个不含骨干网络的Transformer网络。
它将输入图像序列化，并将局部特征直接作为每个独立令牌输入编码器。
Transformer自注意力网络提供全局信息，能够准确获取输入图像令牌之间的上下文关系。
然而，由于Transformer缺乏局部特征建模能力，需要包含每个令牌的局部特征以及相邻令牌之间的信息。
LIE-T2T（局部信息增强-T2T）模块通过重组和展开相邻补丁，并在展开后关注每个补丁的通道维度来解决这一问题。
在Figure 5中，右上角的方块表示WB-DETR的LIE-T2T模块。
LIE-T2T模块的迭代过程如下：
<!-- BLOCK_END: b_101 -->

<!-- BLOCK: b_102 | type: equation | heading: Object Detection with Transformers: A Review > 3.8. WB-DETR -->
$$
P = s t r e t c h ( r e s h a p e ( P i ) ) ,\tag{15}
$$
<!-- BLOCK_END: b_102 -->

<!-- BLOCK: b_103 | type: equation | heading: Object Detection with Transformers: A Review > 3.8. WB-DETR -->
$$
Q = s i g ( e _ { 2 } \cdot R e L U ( e _ { 1 } \cdot P ) ) ,\tag{16}
$$
<!-- BLOCK_END: b_103 -->

<!-- BLOCK: b_104 | type: equation | heading: Object Detection with Transformers: A Review > 3.8. WB-DETR -->
$$
P _ { i + 1 } = e _ { 3 } \cdot ( P \cdot Q ) ,\tag{17}
$$
<!-- BLOCK_END: b_104 -->

<!-- BLOCK: b_105 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.8. WB-DETR -->
其中reshape函数将$\left( l _ { 1 } \times c _ { 1 } \right)$个补丁重组为$\left( h _ { i } \times w _ { i } \times c _ { i } \right)$个特征图。
stretch项表示将$\left( h _ { i } \times w _ { i } \times c _ { i } \right)$个特征图展开为$\left( l _ { 2 } \times c _ { 2 } \right)$个补丁。
此处，全连接层参数为$e _ { 1 } , e _ { 2 }$，$e _ { 3 } .$。
ReLU激活是其非线性映射函数，sig生成最终的注意力。
该模块中的通道注意力提供局部信息，因为补丁通道之间的关系与特征图像素中的空间关系相同。
<!-- BLOCK_END: b_105 -->

<!-- BLOCK: b_106 | type: figure_caption | heading: Object Detection with Transformers: A Review > 3.8. WB-DETR -->
![](Images_GFP684MN/c3ab6bc56c1b38c75e84fd30c9cebab649faa4a81bb0637a11c0fbd75f681c16.jpg) Figure 5。
添加WB-DETR [26]、PnP-DETR [27]和Dynamic-DETR [28]后的原始DETR结构。
此处，网络是一个简单的DETR网络，改进部分用小的彩色方块标示。
品红色方块表示WB-DETR，蓝色方块表示PnP-DETR，绿色方块表示Dynamic-DETR。
<!-- BLOCK_END: b_106 -->

<!-- BLOCK: b_107 | type: heading | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
## 3.9.
PnP-DETR
<!-- BLOCK_END: b_107 -->

<!-- BLOCK: b_108 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
Transformer处理被转换为一维特征向量的图像特征图以产生最终结果。
尽管有效，但由于对背景区域的无用计算，使用完整特征图的代价很高。
PnP-DETR [27]提出了一种轮询与池化（PnP）采样模块，以减少空间冗余并使Transformer网络的计算更加高效。
该模块将图像特征图分为上下文背景特征和精细前景目标特征。
然后，Transformer网络使用这些更新后的特征图并将其转化为最终检测结果。
在Figure 5中，左下方的方块表示PnP-DETR。
该PnP采样模块包含两种采样器：池化采样器和轮询采样器，如下所述。
轮询采样器：轮询采样器提供精细特征向量$\mathbb { V } _ { f }$。
使用元评分模块来查找每个空间位置(x, y)的信息值：
<!-- BLOCK_END: b_108 -->

<!-- BLOCK: b_110 | type: equation | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
$$
a _ { x y } = S c o r e N e t ( v _ { x y } , \theta s ) .\tag{18}
$$
<!-- BLOCK_END: b_110 -->

<!-- BLOCK: b_111 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
评分值与特征向量$v _ { x y }$的信息直接相关。
这些评分值按如下方式排序：
<!-- BLOCK_END: b_111 -->

<!-- BLOCK: b_112 | type: equation | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
$$
[ a _ { z } , | z = 1 , . . . , Z ] , \aleph = S o r t ( a _ { x y } ) ,\tag{19}
$$
<!-- BLOCK_END: b_112 -->

<!-- BLOCK: b_113 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
其中$Z = h _ { i } w _ { i } ,$，ℵ为排序顺序。
选择得分最高的$N _ { s }$个向量以获得精细特征：
<!-- BLOCK_END: b_113 -->

<!-- BLOCK: b_114 | type: equation | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
$$
\mathbb { V } _ { f } = [ v _ { z } , | z = 1 , . . . , N _ { s } ] .\tag{20}
$$
<!-- BLOCK_END: b_114 -->

<!-- BLOCK: b_115 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
此处，预测的信息值被视为调制因子，用于对精细特征向量进行采样：
<!-- BLOCK_END: b_115 -->

<!-- BLOCK: b_116 | type: equation | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
$$
\mathbb { V } _ { f } = [ v _ { z } \times a _ { z } , | z = 1 , . . . , N _ { s } ] .\tag{21}
$$
<!-- BLOCK_END: b_116 -->

<!-- BLOCK: b_117 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
为了使学习稳定，对特征向量进行归一化：
<!-- BLOCK_END: b_117 -->

<!-- BLOCK: b_118 | type: equation | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
$$
\mathbb { V } _ { f } = [ L _ { n o r m } ( v _ { z } ) \times a _ { z } , | z = 1 , . . . , N _ { s } ] .\tag{22}
$$
<!-- BLOCK_END: b_118 -->

<!-- BLOCK: b_119 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
此处，$L _ { n o r m }$为层归一化，$N _ { s } = \alpha Z ,$，其中α为轮询比例因子。
该采样模块减少了训练计算量。
池化采样器：池化采样器获取前景目标的精细特征。
池化采样器压缩背景区域中提供上下文信息的剩余特征向量。
受双重注意力操作[210]和双线性池化[211]的启发，它执行加权池化以获得少量背景特征$M _ { b }$。
背景区域的剩余特征向量如下：
<!-- BLOCK_END: b_119 -->

<!-- BLOCK: b_122 | type: equation | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
$$
\mathbb { V } _ { b } = \mathbb { V } \backslash \mathbb { V } _ { f } = \{ \mathbf { v } _ { b } , | b = 1 , . . . , Z - N \} .\tag{23}
$$
<!-- BLOCK_END: b_122 -->

<!-- BLOCK: b_123 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
聚合权重${ \bf a _ { b } } \in \mathbb { R } ^ { M _ { \mathrm { b } } }$通过将特征与权值$\mathbf { w } ^ { s } \in \mathbb { R } ^ { c _ { i } \times M _ { b } }$投影获得，如下所示：
<!-- BLOCK_END: b_123 -->

<!-- BLOCK: b_124 | type: equation | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
$$
\begin{array} { r } { \mathbf { a } _ { b } = \mathbf { v } _ { b } \mathbf { w } ^ { s } . } \end{array}\tag{24}
$$
<!-- BLOCK_END: b_124 -->

<!-- BLOCK: b_125 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
具有可学习权重$\mathbf { w } ^ { p } \in \mathbb { R } ^ { c _ { i } \times c _ { i } }$的投影特征如下获得：
<!-- BLOCK_END: b_125 -->

<!-- BLOCK: b_126 | type: equation | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
$$
\begin{array} { r } { \dot { \mathbf { v } } _ { b } = \mathbf { v _ { b } } \mathbf { w } ^ { \mathbf { p } } . } \end{array}\tag{25}
$$
<!-- BLOCK_END: b_126 -->

<!-- BLOCK: b_127 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
聚合权重在未采样区域上通过Softmax进行归一化，如下所示：
<!-- BLOCK_END: b_127 -->

<!-- BLOCK: b_128 | type: equation | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
$$
a _ { b m } = \frac { e _ { b m } ^ { a } } { \sum _ { \hat { b } = 1 } ^ { N - Z } e ^ { a } \hat { b } m } .\tag{26}
$$
<!-- BLOCK_END: b_128 -->

<!-- BLOCK: b_129 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
通过使用归一化聚合权重，获得新的特征向量为未采样区域提供信息：
<!-- BLOCK_END: b_129 -->

<!-- BLOCK: b_130 | type: equation | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
$$
\mathbf { v } _ { m } = \sum _ { b = 1 } ^ { Z - N } \hat { \mathbf { v } } _ { b } \times a _ { b m } .\tag{27}
$$
<!-- BLOCK_END: b_130 -->

<!-- BLOCK: b_131 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
考虑所有Z个聚合权重，粗粒度背景上下文特征向量如下：
<!-- BLOCK_END: b_131 -->

<!-- BLOCK: b_132 | type: equation | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
$$
\mathbb { V } _ { c } = \{ \mathbf { v } _ { m } , | b = 1 , . . . , M _ { b } \} .\tag{28}
$$
<!-- BLOCK_END: b_132 -->

<!-- BLOCK: b_133 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.9. PnP-DETR -->
池化采样器利用聚合权重在不同尺度上提供上下文信息。
此处，部分特征向量可能提供局部上下文，而其他特征向量可能捕获全局上下文。
<!-- BLOCK_END: b_133 -->

<!-- BLOCK: b_134 | type: heading | heading: Object Detection with Transformers: A Review > 3.10. Dynamic-DETR -->
## 3.10.
Dynamic-DETR
<!-- BLOCK_END: b_134 -->

<!-- BLOCK: b_135 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.10. Dynamic-DETR -->
Dynamic-DETR [28]在DETR的编码器-解码器网络中引入动态注意力，以解决训练收敛缓慢和小目标检测问题。
首先，提出了一种卷积动态编码器，为编码器网络的自注意模块提供不同的注意力类型，以加快训练收敛。
该编码器的注意力取决于多种因素，如空间效应、尺度效应和输入特征维度效应。
其次，在解码器网络中用交叉注意力替代了基于ROI的动态注意力。
该解码器有助于关注小目标，降低学习难度，并使网络更快收敛。
在Figure 5中，右下方的方块表示Dynamic-DETR。
该动态编码器-解码器网络详细说明如下。
动态编码器：Dynamic-DETR对自注意模块采用卷积方法。
给定特征向量$F = \{ F 1 , \cdots , F _ { n } \}$，其中n=5表示来自特征金字塔的目标检测器，多尺度自注意力（MSA）如下：
<!-- BLOCK_END: b_135 -->

<!-- BLOCK: b_137 | type: equation | heading: Object Detection with Transformers: A Review > 3.10. Dynamic-DETR -->
$$
A t t n = M S A ( F ) . F .\tag{29}
$$
<!-- BLOCK_END: b_137 -->

<!-- BLOCK: b_138 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.10. Dynamic-DETR -->
然而，由于FPN产生的多尺度特征图，这是不可能实现的。
使用二维卷积在相邻尺度间均衡不同尺度的特征图，如金字塔卷积[212]所述。
它关注未调整大小的中间层的空间位置，并将信息传递到其尺度相邻层。
此外，应用SE [213]来组合特征以提供尺度注意力。
动态解码器：动态解码器使用混合注意块替代多头层，以简化交叉注意力网络中的学习并改善小目标检测。
受自然语言处理（NLP）中ConvBERT [214]的启发，它还使用动态卷积替代交叉注意力层。
首先，在解码器网络中引入RoI池化[1]，之后用框编码$B E \in \mathbb { R } ^ { p \times 4 }$替代位置嵌入作为图像尺寸。
动态编码器的输出与框编码$B E ,$一起输入动态解码器，从特征金字塔中池化图像特征$R \in \mathbb { R } ^ { p \times s \times s \times c _ { i } }$，如下所示：
<!-- BLOCK_END: b_138 -->

<!-- BLOCK: b_140 | type: equation | heading: Object Detection with Transformers: A Review > 3.10. Dynamic-DETR -->
$$
R = R o I _ { p o o l } ( F _ { e n c o d e r } , B E , s ) ,\tag{30}
$$
<!-- BLOCK_END: b_140 -->

<!-- BLOCK: b_141 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.10. Dynamic-DETR -->
其中s为池化参数的大小，$c _ { i }$表示$F _ { e n c o d e r }$的通道数。
为了将其输入交叉注意力模块，目标查询需要输入嵌入$q e \in R ^ { p \times c _ { i } }$。
这些嵌入通过多头自注意力（MHSAttn）层传递，如下所示：
<!-- BLOCK_END: b_141 -->

<!-- BLOCK: b_142 | type: equation | heading: Object Detection with Transformers: A Review > 3.10. Dynamic-DETR -->
$$
q e ^ { * } = M H S A t t n ( q e , q e , q e ) .\tag{31}
$$
<!-- BLOCK_END: b_142 -->

<!-- BLOCK: b_143 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.10. Dynamic-DETR -->
然后，这些查询嵌入通过全连接层（动态滤波器）传递，如下所示：
<!-- BLOCK_END: b_143 -->

<!-- BLOCK: b_144 | type: equation | heading: Object Detection with Transformers: A Review > 3.10. Dynamic-DETR -->
$$
F i l t e r ^ { q e } = F C ( q e ^ { * } ) .\tag{32}
$$
<!-- BLOCK_END: b_144 -->

<!-- BLOCK: b_145 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.10. Dynamic-DETR -->
最后，使用动态滤波器$F i l t e r ^ { q e }$通过1×1卷积执行特征与目标查询之间的交叉注意力
<!-- BLOCK_END: b_145 -->

<!-- BLOCK: b_146 | type: equation | heading: Object Detection with Transformers: A Review > 3.10. Dynamic-DETR -->
$$
q e ^ { F } = C o n _ { 1 \times 1 } ( F , F i l t e r ^ { q e } ) .\tag{33}
$$
<!-- BLOCK_END: b_146 -->

<!-- BLOCK: b_147 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.10. Dynamic-DETR -->
这些特征通过FFN层传递，以提供多种预测结果，包括更新的目标嵌入、更新的框编码和目标类别。
该过程通过先聚焦稀疏区域再扩展到全局区域，简化了交叉注意力模块的学习。
<!-- BLOCK_END: b_147 -->

<!-- BLOCK: b_148 | type: heading | heading: Object Detection with Transformers: A Review > 3.11. YOLOS-DETR -->
## 3.11.
YOLOS-DETR
<!-- BLOCK_END: b_148 -->

<!-- BLOCK: b_149 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.11. YOLOS-DETR -->
视觉Transformer（ViT）[8]继承自NLP，在图像识别任务上表现良好。
ViT-FRCNN [215]使用预训练的骨干网络（ViT）用于基于CNN的检测器。
它利用卷积神经网络，依赖强二维归纳偏置和逐区域池化操作进行目标级感知。
其他类似工作，如DETR [11]，使用CNN和金字塔特征引入二维归纳偏置。
YOLOS-DETR [29]展示了Transformer从图像识别到序列维度检测的可迁移性和多功能性，使用关于输入空间设计的最少信息。
它紧密遵循ViT架构，并进行了两处简单修改。
首先，它移除了图像分类补丁（CLS），并添加了随机初始化的一百个检测补丁（DET）[216]，以及用于目标检测的输入补丁嵌入。
其次，与DETR类似，使用二分匹配损失替代ViT分类损失。
Transformer编码器将生成的序列作为输入，如下所示：
<!-- BLOCK_END: b_149 -->

<!-- BLOCK: b_150 | type: equation | heading: Object Detection with Transformers: A Review > 3.11. YOLOS-DETR -->
$$
\begin{array} { r } { s _ { 0 } = [ \mathbf { I } _ { p } ^ { 1 } \mathbf { L } ; \cdot \cdot \cdot ; \mathbf { I } _ { p } ^ { M } \mathbf { L } ; \mathbf { I } _ { d } ^ { 1 } ; \cdot \cdot \cdot ; \mathbf { I } _ { d } ^ { 1 0 0 } ] + \mathbf { P E } , } \end{array}\tag{34}
$$
<!-- BLOCK_END: b_150 -->

<!-- BLOCK: b_151 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.11. YOLOS-DETR -->
其中I为输入图像$\mathbf { I } \in \mathbb { R } ^ { h _ { i } \times w _ { i } \times c _ { i } }$，被重塑为二维令牌$\mathbf { I } _ { p } \in \mathbb { R } ^ { n _ { i } \times ( R ^ { 2 } \cdot c _ { i } ) }$此处，$h _ { i }$表示高度，$w _ { i }$表示输入图像的宽度。
$c _ { i }$为通道总数。
$( r , r )$为每个令牌的分辨率，$\begin{array} { r } { n _ { i } = \frac { h _ { i } w _ { i } } { r ^ { 2 } } } \end{array}$为令牌总数。
这些令牌通过线性投影映射到$D _ { i }$维，$\mathbf { L } \in \mathbb { R } ^ { ( r ^ { 2 } \cdot c _ { i } ) \times D _ { i } }$该投影的结果为$\mathbf { I } _ { p } \mathbf { L }$。
编码器还接收一百个随机初始化的可学习令牌$\mathbf { I } _ { d } \in \mathbb { R } ^ { 1 0 0 \times D _ { i } }$。
为保留位置信息，还添加了位置嵌入$\mathbf { P E } \in \mathbb { R } ^ { ( n _ { i } + 1 0 0 ) \times D _ { i } }$。
Transformer的编码器包含多头自注意力机制和一个MLP块，使用GELU [217]非线性激活函数。
层归一化（LN）[218]添加在每个自注意力和MLP块之间，如下所示：
<!-- BLOCK_END: b_151 -->

<!-- BLOCK: b_153 | type: equation | heading: Object Detection with Transformers: A Review > 3.11. YOLOS-DETR -->
$$
\begin{array} { r l } { \acute { s } _ { n } } & { { } = M H S A t t n ( L N ( s _ { n - 1 } ) ) + s _ { n - 1 } , } \end{array}\tag{35}
$$
<!-- BLOCK_END: b_153 -->

<!-- BLOCK: b_154 | type: equation | heading: Object Detection with Transformers: A Review > 3.11. YOLOS-DETR -->
$$
\begin{array} { r l } { s _ { n } } & { { } = M L P ( L N ( \acute { s } _ { n } ) ) + \acute { s } _ { n } , } \end{array}\tag{36}
$$
<!-- BLOCK_END: b_154 -->

<!-- BLOCK: b_155 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.11. YOLOS-DETR -->
其中$s _ { n }$为编码器输入序列。
在Figure 6中，右上角的方块表示YOLOS-DETR。
<!-- BLOCK_END: b_155 -->

<!-- BLOCK: b_156 | type: figure_caption | heading: Object Detection with Transformers: A Review > 3.11. YOLOS-DETR -->
![](Images_GFP684MN/71a9e6b3c55efe5d187d458daff9c72bb0d7baaee7ae6d991e6189a8ff5a45ab.jpg) Figure 6。
添加YOLOS-DETR [29]、Anchor-DETR [30]和Sparse-DETR [31]后的原始DETR结构。
此处，网络是一个简单的DETR网络，改进部分用小的彩色方块标示。
黄色方块表示YOLOS-DETR，浅蓝色方块表示Anchor-DETR，浅橙色方块表示Sparse-DETR。
<!-- BLOCK_END: b_156 -->

<!-- BLOCK: b_157 | type: heading | heading: Object Detection with Transformers: A Review > 3.12. Anchor-DETR -->
## 3.12.
Anchor-DETR
<!-- BLOCK_END: b_157 -->

<!-- BLOCK: b_158 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.12. Anchor-DETR -->
DETR使用可学习嵌入作为解码器网络中的目标查询。
这些输入嵌入没有明确的物理意义，无法说明应关注何处。
由于目标查询集中于非特定区域，优化网络具有挑战性。
Anchor-DETR [30]通过提出将目标查询作为锚点来解决这一问题，锚点在基于CNN的目标检测器中被广泛使用。
这种查询设计可以在一个区域提供多个目标预测。
此外，还提出了对注意力的若干修改，以降低内存成本并提高性能。
在Figure 6中，黄色方块展示了Anchor-DETR。
Anchor-DETR的两个主要贡献——查询设计和注意力变体设计——说明如下。
行列解耦注意力：DETR需要大量GPU内存，如[219,220]所述，这是由于交叉注意力模块的复杂性。
它比解码器中的自注意力模块更为复杂。
尽管Deformable-DETR降低了内存成本，但仍会导致随机内存访问，使网络变慢。
行列解耦注意力（RCDA），如Figure 6蓝色方块所示，减少了内存消耗并提供了相当或更好的效率。
锚点作为目标查询：基于CNN的目标检测器将锚点视为输入特征图的相对位置。
相比之下，基于Transformer的检测器采用均匀网格位置、手工设计位置或学习位置作为锚点。
Anchor-DETR考虑两种类型的锚点：学习锚位置和网格锚位置。
网格锚位置为输入图像的网格点。
学习锚位置为从0到1的均匀分布（随机初始化），并使用学习参数进行更新。
<!-- BLOCK_END: b_158 -->

<!-- BLOCK: b_161 | type: heading | heading: Object Detection with Transformers: A Review > 3.13. Sparse-DETR -->
## 3.13.
Sparse-DETR
<!-- BLOCK_END: b_161 -->

<!-- BLOCK: b_162 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.13. Sparse-DETR -->
Sparse-DETR [31]通过可学习的交叉注意力图预测器过滤编码器令牌。
在解码器网络中区分这些令牌后，它仅关注前景令牌以降低计算成本。
Sparse-DETR引入了评分模块、编码器中的辅助头和解码器的Top-k查询选择模块。
在Figure 6中，浅橙色方块表示Sparse-DETR。
首先，它使用评分网络确定输入到编码器的令牌的显著性，选择前$\rho \%$个令牌。
其次，辅助头从编码器网络的输出中获取前k个令牌。
最后，前k个令牌被用作解码器目标查询。
显著令牌预测模块使用阈值$\rho$对从骨干特征图中提取的编码器令牌进行细化，并更新特征$x _ { l } - 1$，如下所示：
<!-- BLOCK_END: b_162 -->

<!-- BLOCK: b_164 | type: equation | heading: Object Detection with Transformers: A Review > 3.13. Sparse-DETR -->
$$
\begin{array} { r } { x _ { 1 } ^ { \mathbf { m } } = \left\{ \begin{array} { l l } { x _ { l - 1 } ^ { m } } & { m \not \in \Omega _ { r } ^ { q } } \\ { L N \big ( F F N ( y _ { l } ^ { m } ) + y _ { l } ^ { m } \big ) } & { m \in \Omega _ { r } ^ { q } , } \end{array} \right. } \\ { w h e r e } & { y _ { l } ^ { m } = L N \big ( D e f o r m A t t n ( x _ { l - 1 } ^ { m } , x _ { l - 1 } \big ) + x _ { l - 1 } ^ { m } \big ) , } \end{array}\tag{37}
$$
<!-- BLOCK_END: b_164 -->

<!-- BLOCK: b_165 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.13. Sparse-DETR -->
其中DeformAttn为可变形注意力，FFN为前馈网络，LN为层归一化。
然后，解码器交叉注意力图（DAM）累积解码器目标查询的注意力权重，网络通过最小化预测与二值化DAM之间的损失进行训练，如下所示：
<!-- BLOCK_END: b_165 -->

<!-- BLOCK: b_166 | type: equation | heading: Object Detection with Transformers: A Review > 3.13. Sparse-DETR -->
$$
\mathcal { L } _ { d a m } = \frac { - 1 } { M } \sum _ { k = 1 } ^ { M } B C E L o s s ( s n ( x _ { f } ) , D A M _ { k } ^ { b } ) ,\tag{38}
$$
<!-- BLOCK_END: b_166 -->

<!-- BLOCK: b_167 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.13. Sparse-DETR -->
其中BCELoss为二元交叉熵（BCE）损失，$D A M _ { k } ^ { b }$为编码器令牌的第k个二值化DAM值，sn为评分网络。
通过这种方式，sparse-DETR通过显著减少编码器令牌来最小化计算量。
<!-- BLOCK_END: b_167 -->

<!-- BLOCK: b_168 | type: heading | heading: Object Detection with Transformers: A Review > 3.14. $D ^ { 2 }$ ETR -->
## 3.14.
$D ^ { 2 }$ ETR
<!-- BLOCK_END: b_168 -->

<!-- BLOCK: b_169 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.14. $D ^ { 2 }$ ETR -->
许多工作[20,22–25]通过修改交叉注意力模块来加快训练收敛。
许多研究者[20]使用多尺度特征图来提升小目标的性能。
然而，针对高计算复杂度问题的解决方案尚未被提出。
D2ETR [32]以较低的计算成本实现了更好的性能。
在没有编码器模块的情况下，解码器直接使用骨干网络提供的精细融合特征图，配合新颖的跨尺度注意力模块。
D2ETR包含两个主要模块：骨干网络和解码器。
基于金字塔视觉Transformer（PVT）的骨干网络由两个并行层组成：一个用于跨尺度交互，另一个用于尺度内交互。
该骨干网络包含四个Transformer层级，以提供多尺度特征图。
所有层级具有相同的架构，取决于所选Transformer的基本模块。
骨干网络还包含三个与四个Transformer层级并行的融合层级。
这些融合层级提供输入特征的跨尺度融合。
第i个融合层级如Figure 7中浅绿色方块所示。
跨尺度注意力的公式如下：
<!-- BLOCK_END: b_169 -->

<!-- BLOCK: b_170 | type: equation | heading: Object Detection with Transformers: A Review > 3.14. $D ^ { 2 }$ ETR -->
$$
f _ { j } = \mathbf { L } _ { j } ( f _ { j - 1 } ) ,\tag{39}
$$
<!-- BLOCK_END: b_170 -->

<!-- BLOCK: b_171 | type: equation | heading: Object Detection with Transformers: A Review > 3.14. $D ^ { 2 }$ ETR -->
$$
f _ { j } ^ { \ast } = S A ( f _ { q } , f _ { k } , f _ { v } ) ,\tag{40}
$$
<!-- BLOCK_END: b_171 -->

<!-- BLOCK: b_172 | type: equation | heading: Object Detection with Transformers: A Review > 3.14. $D ^ { 2 }$ ETR -->
$$
f _ { q } = f _ { j } , f _ { k } = f _ { v } = [ f _ { 1 } ^ { * } , f _ { 2 } ^ { * } , \ldots , f _ { j - 1 } ^ { * } , f _ { j } ] ,\tag{41}
$$
<!-- BLOCK_END: b_172 -->

<!-- BLOCK: b_173 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.14. $D ^ { 2 }$ ETR -->
其中$f _ { j } ^ { * }$为融合后的特征图$f _ { j } .$给定L作为解码器的输入即最高层级特征图，跨尺度注意力的最终结果为$f _ { 1 } ^ { * } , f _ { 2 } ^ { * } , \ldots , f _ { L } ^ { * }$。
该骨干网络的输出被送入解码器，解码器同时接收目标查询。
它提供输出嵌入，由前馈网络独立转换为类别标签和边界框坐标。
在没有编码器模块的情况下，解码器直接使用骨干网络提供的精细融合特征图，配合新颖的跨尺度注意力模块，以较低的计算成本实现更好的性能。
<!-- BLOCK_END: b_173 -->

<!-- BLOCK: b_174 | type: figure_caption | heading: Object Detection with Transformers: A Review > 3.14. $D ^ { 2 }$ ETR -->
![](Images_GFP684MN/efd2b5160235229e6876e2db5da9d069ea1cb7627413b0a9242a2a0de9dfe6e9.jpg) Figure 7。
添加D2ETR [32]、FP-DETR [33]和CF-DETR [34]后的原始DETR结构。
此处，网络是一个简单的DETR网络，改进部分用小的彩色方块标示。
浅绿色方块表示D2ETR，粉色方块表示FP-DETR，蓝色方块表示CF-DETR。
<!-- BLOCK_END: b_174 -->

<!-- BLOCK: b_175 | type: heading | heading: Object Detection with Transformers: A Review > 3.15. FP-DETR -->
## 3.15.
FP-DETR
<!-- BLOCK_END: b_175 -->

<!-- BLOCK: b_176 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.15. FP-DETR -->
现代基于CNN的检测器，如YOLO [221]和Faster-RCNN [1]，利用在ImageNet上预训练的骨干网络之上的专用层，以享受预训练带来的好处，如改进的性能和更快的训练收敛。
DETR网络及其改进版本[21]仅预训练其骨干网络，同时从头训练编码器和解码器层。
因此，Transformer需要大量训练数据进行微调。
不对检测Transformer进行预训练的主要原因是预训练任务与最终检测任务之间的差异。
首先，Transformer的解码器模块接收多个目标查询作为输入以检测目标，而ImageNet分类仅接受单个查询（类别令牌）。
其次，自注意力模块和交叉注意力模块中对输入查询嵌入的投影容易对单个类别查询过拟合，使得解码器网络难以预训练。此外，下游检测任务关注分类和定位，而上游任务仅考虑感兴趣目标的分类。
FP-DETR [33]重新制定了检测Transformer的预训练和微调阶段。
在Figure 7中，粉色方块表示FP-DETR。
它仅采用检测Transformer的编码器网络进行预训练，因为在ImageNet分类任务上预训练解码器具有挑战性。
此外，DETR同时使用编码器和CNN骨干网络作为特征提取器。
FP-DETR用多尺度分词器替代CNN骨干网络，并使用编码器网络提取特征。
它在ImageNet数据集上完全预训练Deformable-DETR，并对其进行微调以完成最终检测，实现了有竞争力的性能。
<!-- BLOCK_END: b_176 -->

<!-- BLOCK: b_178 | type: heading | heading: Object Detection with Transformers: A Review > 3.16. CF-DETR -->
## 3.16.
CF-DETR
<!-- BLOCK_END: b_178 -->

<!-- BLOCK: b_179 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.16. CF-DETR -->
CF-DETR [34]观察到在低IoU阈值下，检测Transformer上基于COCO风格的度量平均精度（AP）对小目标的结果优于基于CNN的检测器。
它通过利用局部信息来细化预测位置，因为不正确的边界框位置会降低小目标的性能。
CF-DETR将Transformer增强的FPN（TEF）模块、粗层和细层引入DETR的解码器网络。
在Figure 7中，蓝色方块表示CF-DETR。
TEF模块提供与FPN相同的功能，具有从骨干网络提取的非局部特征E4和E4，以及从编码器输出获取的E5特征。
TEF模块和编码器网络的特征作为输入送入解码器。
解码器模块引入了粗块和细块。
粗块从全局上下文中选择前景特征。
细块包含两个模块：自适应尺度融合（ASF）和局部交叉注意力（LCA），进一步细化粗框。
总之，这些模块通过融合全局和局部信息来细化和丰富特征，以提升检测Transformer的性能。
<!-- BLOCK_END: b_179 -->

<!-- BLOCK: b_180 | type: heading | heading: Object Detection with Transformers: A Review > 3.17. DAB-DETR -->
## 3.17.
DAB-DETR
<!-- BLOCK_END: b_180 -->

<!-- BLOCK: b_181 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.17. DAB-DETR -->
DAB-DETR [72]将边界框坐标作为解码器中的目标查询，并在每一层中逐步更新。
在Figure 8中，紫色方块表示DAB-DETR。
这些边界框坐标通过提供位置信息并利用高度和宽度值更新位置注意力图，使训练收敛更快。
这类目标查询在注意力机制之前提供了更优的空间信息先验，并提供了一种简单的查询构建机制。
<!-- BLOCK_END: b_181 -->

<!-- BLOCK: b_182 | type: figure_caption | heading: Object Detection with Transformers: A Review > 3.17. DAB-DETR -->
![](Images_GFP684MN/9c3e4a57096bb1f03483aa216c98eb81a123bf892b35fc6ae6d6683f955b1cf3.jpg) Figure 8。
添加DAB-DETR [72]、DN-DETR [35]和AdaMixer [36]后原始DETR的结构。
此处，网络为简单的DETR网络，改进部分以小彩色方块标示。
紫色方块表示DAB-DETR，深绿色方块表示DN-DETR，浅绿色方块表示AdaMixer。
<!-- BLOCK_END: b_182 -->

<!-- BLOCK: b_183 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.17. DAB-DETR -->
解码器网络包含两个主要网络：用于更新查询的自注意力网络和用于寻找特征探测的交叉注意力网络。
原始DETR的自注意力与DAB-DETR的区别在于，查询矩阵和键矩阵还包含从边界框坐标中获取的位置信息。
交叉注意力模块将键矩阵和查询矩阵中的位置信息与内容信息进行拼接，并确定其对应的头。
解码器将输入嵌入作为内容查询，将锚框作为位置查询，以查找与锚点和内容查询相关的目标概率。
这样，用作目标查询的动态边界框坐标提供了更好的预测，使训练收敛更快，并提升了小目标的检测结果。
<!-- BLOCK_END: b_183 -->

<!-- BLOCK: b_184 | type: heading | heading: Object Detection with Transformers: A Review > 3.18. DN-DETR -->
## 3.18.
DN-DETR
<!-- BLOCK_END: b_184 -->

<!-- BLOCK: b_185 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.18. DN-DETR -->
DN-DETR [35]使用加噪的目标查询作为解码器的额外输入，以降低DETR中二分匹配机制的不稳定性，该不稳定性导致了收敛缓慢的问题。
在Figure 8中，深绿色方块表示DN-DETR。
解码器查询包含两部分：去噪部分，包含加噪的真实标注框-标签对作为输入；匹配部分，包含可学习的锚点作为输入。
匹配部分$M = \left\{ M _ { 0 } , M _ { 1 } , \dots , M _ { l - 1 } \right\}$确定真实标注标签对与解码器输出之间的相似性，而去噪部分$d = \{ d _ { 0 } , d _ { 1 } , \dotsc , d _ { k - 1 } \}$尝试如下重构真实标注目标：
<!-- BLOCK_END: b_185 -->

<!-- BLOCK: b_186 | type: equation | heading: Object Detection with Transformers: A Review > 3.18. DN-DETR -->
$$
O u t p u t = D e c o d e r ( d , M , I | A ) ,\tag{42}
$$
<!-- BLOCK_END: b_186 -->

<!-- BLOCK: b_187 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.18. DN-DETR -->
其中I是从Transformer编码器输入中获取的图像特征，A是阻止匹配部分与去噪部分之间以及同一真实标注对象不同噪声级别之间信息传递的注意力掩码。
解码器包含真实标注对象的噪声级别，其中对边界框和类别标签添加噪声，例如标签翻转。
它包含一个超参数λ用于控制噪声级别。
DN-DETR的训练架构基于DAB-DETR，因为它同样将边界框坐标作为目标查询。
这两种架构之间唯一的区别是类别标签指示器作为解码器中的额外输入以辅助标签去噪。
在DAB-DETR中边界框的更新方式不一致，使得相对偏移学习具有挑战性。
DN-DETR中的去噪训练机制提升了性能和训练收敛速度。
<!-- BLOCK_END: b_187 -->

<!-- BLOCK: b_188 | type: heading | heading: Object Detection with Transformers: A Review > 3.19. AdaMixer -->
## 3.19.
AdaMixer
<!-- BLOCK_END: b_188 -->

<!-- BLOCK: b_189 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.19. AdaMixer -->
AdaMixer [36]将编码器视为骨干网络与解码器之间的额外网络，由于其设计复杂性，该网络限制了性能并减缓了训练收敛。
AdaMixer提供了一种无需编码器的检测Transformer网络。
在Figure 8中，浅绿色方块表示AdaMixer。
AdaMixer的主要模块说明如下。
三维特征空间：对于三维特征空间，来自CNN骨干网络的输入特征图（下采样步长为$s _ { i } ^ { f }$）首先通过线性层转换为相同的$d _ { f }$通道，并计算其z轴坐标如下：
<!-- BLOCK_END: b_189 -->

<!-- BLOCK: b_191 | type: equation | heading: Object Detection with Transformers: A Review > 3.19. AdaMixer -->
$$
z _ { i } ^ { f } = l o g _ { 2 } ( s _ { i } ^ { f } / s _ { b } ) ,\tag{43}
$$
<!-- BLOCK_END: b_191 -->

<!-- BLOCK: b_192 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.19. AdaMixer -->
其中特征图的高度$h _ { i }$和宽度$w _ { i }$（不同步长）被重新缩放为$h _ { i } / s _ { b }$和$w _ { i } / s _ { b } ,$，其中$s _ { b } = 4$三维特征采样过程：在采样过程中，查询生成$I _ { p }$组向量对应$I _ { p }$个采样点，$( \Delta x _ { j } , \Delta y _ { j } , \Delta z _ { j } ) I _ { p } ,$，其中每个向量通过线性层$L _ { i }$依赖于其内容向量$q _ { i }$如下：
<!-- BLOCK_END: b_192 -->

<!-- BLOCK: b_194 | type: equation | heading: Object Detection with Transformers: A Review > 3.19. AdaMixer -->
$$
( \Delta x _ { j } , \Delta y _ { j } , \Delta z _ { j } ) I _ { p } = L _ { i } ( q _ { i } ) .\tag{44}
$$
<!-- BLOCK_END: b_194 -->

<!-- BLOCK: b_195 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.19. AdaMixer -->
这些偏移值相对于目标查询的位置向量转换为采样位置如下：
<!-- BLOCK_END: b_195 -->

<!-- BLOCK: b_196 | type: equation | heading: Object Detection with Transformers: A Review > 3.19. AdaMixer -->
$$
\left\{ \begin{array} { l l } { \tilde { x } _ { j } } & { = x + \Delta x _ { j } . 2 ^ { z - r } , } \\ { \tilde { y } _ { j } } & { = y + \Delta y _ { j } . 2 ^ { z + r } , } \\ { \tilde { z } _ { j } } & { = z + \Delta z _ { j } . } \end{array} \right.\tag{45}
$$
<!-- BLOCK_END: b_196 -->

<!-- BLOCK: b_197 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.19. AdaMixer -->
在三维特征空间上的插值首先在$\left( x _ { i } , y _ { i } \right)$空间中通过双线性插值进行采样，然后在z轴上通过高斯加权进行插值，其中第i个特征图的权重如下：
<!-- BLOCK_END: b_197 -->

<!-- BLOCK: b_198 | type: equation | heading: Object Detection with Transformers: A Review > 3.19. AdaMixer -->
$$
\tilde { w } _ { i } = \frac { e x p ( - ( \tilde { z } - z _ { i } ^ { f } ) ^ { 2 } / \Gamma _ { z } ) } { \sum _ { i } e x p ( - ( \tilde { z } - z _ { i } ^ { f } ) ^ { 2 } / \Gamma _ { z } ) } ,\tag{46}
$$
<!-- BLOCK_END: b_198 -->

<!-- BLOCK: b_199 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.19. AdaMixer -->
其中$\Gamma _ { z }$是用于在z轴$( \Gamma _ { z } = 2 )$上插值的平滑系数。该过程通过根据查询进行特征采样，使解码器的检测学习更加容易。
AdaMixer解码器：AdaMixer中的解码器模块接收内容向量$q _ { i }$和位置向量$\left( x _ { i } , y _ { i } , z _ { i } , r _ { i } \right)$作为输入目标查询。
在这些查询之间应用位置感知多头自注意力如下：
<!-- BLOCK_END: b_199 -->

<!-- BLOCK: b_201 | type: equation | heading: Object Detection with Transformers: A Review > 3.19. AdaMixer -->
$$
A t t n ( q _ { i } , k _ { i } , v _ { i } ) = S o f t m a x ( \frac { q _ { i } k _ { i } ^ { T } } { \sqrt { d } } + \alpha X ) . v _ { i } ,\tag{47}
$$
<!-- BLOCK_END: b_201 -->

<!-- BLOCK: b_202 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.19. AdaMixer -->
其中$X _ { k l } = l o g ( | b o x _ { k } \cap b o x _ { l } / | b o x _ { k } | + \epsilon ) , \epsilon = 1 0 ^ { - 7 } .$。
$X _ { k l } = 0$表示boxk位于$b o x _ { l }$和$X _ { k l } = l$内部，$X _ { k l } = l$表示box${ { x } _ { k } }$和boxl之间无重叠。
该位置向量在解码器网络的每一阶段都会更新。
AdaMixer解码器模块接收内容向量和位置向量作为输入目标查询。
为此，从CNN骨干网络获取的多尺度特征被转换为三维特征空间，因为解码器需要考虑$\left( x _ { i } , y _ { i } \right)$空间，同时应能适配检测目标的尺度变化。
它将该特征空间中的采样特征作为输入。
它应用AdaMixer机制提供输入查询的最终预测，而无需使用编码器网络，以降低检测Transformer的计算复杂度。
<!-- BLOCK_END: b_202 -->

<!-- BLOCK: b_203 | type: heading | heading: Object Detection with Transformers: A Review > 3.20. REGO-DETR -->
## 3.20.
REGO-DETR
<!-- BLOCK_END: b_203 -->

<!-- BLOCK: b_204 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.20. REGO-DETR -->
REGO-DETR [37]提出了一种基于RoI的检测细化方法，以改进DETR中的注意力机制。
在Figure 9中，紫色色块表示REGO-DETR。
它包含两个主要模块：多层循环机制和基于视觉注意的解码器。
在多层循环机制中，前一层级检测到的边界框被用于获取视觉注意特征。
这些特征利用早期注意力转换为描述目标的细化注意力。
第k个处理层级如下：
<!-- BLOCK_END: b_204 -->

<!-- BLOCK: b_205 | type: equation | heading: Object Detection with Transformers: A Review > 3.20. REGO-DETR -->
$$
\left\{ \begin{array} { l l } { \displaystyle O _ { c l a s s } ( k ) = D F _ { c l a s s } ( H _ { d e } ( k ) ) , } \\ { O _ { b b o x } ( k ) = D F _ { b b o x } ( H _ { d e } ( k ) ) + O _ { b b o x } ( k - 1 ) , } \end{array} \right.\tag{48}
$$
<!-- BLOCK_END: b_205 -->

<!-- BLOCK: b_206 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.20. REGO-DETR -->
其中$O _ { c l a s s } \in \mathbb { R } ^ { M _ { d } \times M _ { c } }$，$O _ { b b o x } \in \mathbb { R } ^ { M _ { d } \times 4 }$。
此处，$M _ { d }$和$M _ { c }$分别表示预测目标和类别的总数。
$D F _ { c l a s s }$和$D F _ { b b o x }$是将输入特征转换为所需输出的函数。
$H _ { d e } ( k )$是该层级解码后的注意力，如下所示：
<!-- BLOCK_END: b_206 -->

<!-- BLOCK: b_207 | type: equation | heading: Object Detection with Transformers: A Review > 3.20. REGO-DETR -->
$$
H _ { d e } ( k ) = [ H _ { g m } ( k ) , H _ { d e } ( k - 1 ) ] ,\tag{49}
$$
<!-- BLOCK_END: b_207 -->

<!-- BLOCK: b_208 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.20. REGO-DETR -->
其中$H _ { g m } ( k )$指根据$H _ { d e } ( k - 1 )$及先前层级的视觉注意特征。
这些视觉注意特征通过多头交叉注意力根据先前的注意力输出转换为细化注意力输出，如下所示：
<!-- BLOCK_END: b_208 -->

<!-- BLOCK: b_209 | type: equation | heading: Object Detection with Transformers: A Review > 3.20. REGO-DETR -->
$$
H _ { g m } ( k ) = A t t n ( V ( k ) , H _ { d e } ( k - 1 ) ) .\tag{50}
$$
<!-- BLOCK_END: b_209 -->

<!-- BLOCK: b_210 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.20. REGO-DETR -->
为提取视觉注意特征$V ( k )$，执行以下操作：
<!-- BLOCK_END: b_210 -->

<!-- BLOCK: b_211 | type: equation | heading: Object Detection with Transformers: A Review > 3.20. REGO-DETR -->
$$
V ( k ) = F E _ { e x t } ( X , R I ( { \cal O } _ { b b o x } ( k - 1 ) , \alpha ( k ) ) ) ,\tag{51}
$$
<!-- BLOCK_END: b_211 -->

<!-- BLOCK: b_212 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.20. REGO-DETR -->
其中$F E _ { e x t }$是特征提取函数，$\alpha ( k )$是标量参数，RI是RoI计算。
通过这种方式，基于感兴趣区域（RoI）的细化模块使检测Transformer的训练收敛更快，并提供更好的性能。
<!-- BLOCK_END: b_212 -->

<!-- BLOCK: b_213 | type: figure_caption | heading: Object Detection with Transformers: A Review > 3.20. REGO-DETR -->
![](Images_GFP684MN/974b963dbb7639bd17f5112d7db66dc6bb410ac634f49e4993a0377bbd03b8a2.jpg) Figure 9。
添加REGO-DETR [37]和DINO [38]后原始DETR的结构。
此处，网络为简单的DETR网络，改进部分以小彩色方块标示。
紫色色块表示REGO-DETR，红色指示块表示DINO。
<!-- BLOCK_END: b_213 -->

<!-- BLOCK: b_214 | type: heading | heading: Object Detection with Transformers: A Review > 3.21. DINO -->
## 3.21.
DINO
<!-- BLOCK_END: b_214 -->

<!-- BLOCK: b_215 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.21. DINO -->
DN-DETR对作为目标查询输入解码器的锚点添加正噪声，并仅为附近存在真实标注对象的锚点提供标签。
继DAB-DETR和DN-DETR之后，DINO [38]提出了一种用于锚点初始化的混合目标查询选择方法和用于边界框预测的两次前向查找机制。
它提供了对比去噪（CDN）模块，该模块将位置查询作为锚框并添加额外的去噪损失。
在Figure 9中，红色方块表示DINO。
该检测器使用$\lambda _ { 1 }$和$\lambda _ { 2 }$超参数，其中$\lambda _ { 1 } < \lambda _ { 2 }$。
边界框$\boldsymbol { b } = \left( x _ { i } , y _ { i } , w _ { i } , h _ { i } \right)$作为解码器的输入，其对应生成的锚点记为$a = \left( x _ { i } , y _ { i } , w _ { i } , h _ { i } \right)$
<!-- BLOCK_END: b_215 -->

<!-- BLOCK: b_216 | type: equation | heading: Object Detection with Transformers: A Review > 3.21. DINO -->
$$
\begin{array} { r } { A T D ( k ) = \frac { 1 } { k } \Sigma \{ M _ { K } ( \{ \mid b _ { 0 } - a _ { 0 } \mid _ { 1 } , \mid b _ { 1 } - a _ { 1 } \mid _ { 1 } , . . . , \mid \mid b _ { N - 1 } - a _ { N - 1 } \mid _ { 1 } \} , k ) \} , } \end{array}\tag{52}
$$
<!-- BLOCK_END: b_216 -->

<!-- BLOCK: b_217 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.21. DINO -->
其中$\parallel \left( b _ { i } - a _ { i } \right) \ |$是锚点与边界框之间的距离，$M _ { K } ( { \boldsymbol { x } } , { \boldsymbol { k } } )$是提供x中前K个元素的函数。λ参数是为作为输入目标查询馈入解码器的锚点生成噪声的阈值。
它提供两种类型的锚点查询：正样本，其阈值小于$\lambda _ { 1 }$；负样本，其噪声阈值大于$\lambda _ { 1 }$且小于$\lambda _ { 2 }$。
这样，附近没有真实标注的锚点被标记为"无目标"。
因此，DINO使训练收敛更快，并提升了小目标的性能。
DINOv2 [222]是由Meta AI开发的自监督视觉Transformer模型。
它在包含1.42亿张图像的大规模数据集上进行训练，无需任何标签或标注。
DINOv2 [222]生成高性能的视觉特征，可直接与简单分类器（如线性层）配合使用，应用于多种计算机视觉任务。
这些视觉特征具有鲁棒性，在不同领域之间表现良好，无需微调。
DINOv3 [223]同样由Meta AI开发，是DINO框架的第三代版本。
它是一个拥有70亿参数的视觉Transformer，在1.7十亿张无标签图像上进行训练。
DINOv3 [223]引入了多项创新，包括在训练期间稳定密集特征图的Gram锚定，以及通过抖动增强的轴向RoPE（旋转位置编码），提升了模型对不同图像分辨率、尺度和宽高比的鲁棒性。
这些进展使DINOv3 [223]在目标检测、语义分割和深度估计等广泛的视觉任务上实现了最先进的性能。
<!-- BLOCK_END: b_217 -->

<!-- BLOCK: b_219 | type: heading | heading: Object Detection with Transformers: A Review > 3.22. Co-DETR -->
## 3.22.
Co-DETR
<!-- BLOCK_END: b_219 -->

<!-- BLOCK: b_220 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.22. Co-DETR -->
Co-DETR [39]是对DETR的改进，解决了标准一对一标签分配的一个关键限制，即在DETR中将每个真实标注对象限制为单个预测查询。
在Figure 10中，浅红色方块表示Co-DETR。
这种设计导致训练期间正样本数量很少，许多解码器查询未被利用，梯度流动缓慢，尤其在学习初期。
Co-DETR通过引入协作混合分配策略克服了这一问题，该策略将原始的一对一分配与通过辅助头实现的一对多分配相结合。
一对一分配保持了每个对象的唯一匹配，维持了DETR训练的稳定性和结构。
一对多分配利用经典目标检测器（如ATSS或Faster R-CNN）的启发式方法，将多个预测查询分配给同一真实标注对象，为编码器和解码器提供更密集的监督。
辅助头仅在训练期间活跃，在推理时被丢弃，确保测试时不增加额外计算成本。
总训练损失表示如下：
<!-- BLOCK_END: b_220 -->

<!-- BLOCK: b_222 | type: equation | heading: Object Detection with Transformers: A Review > 3.22. Co-DETR -->
$$
L _ { \mathrm { t o t a l } } = L _ { \mathrm { D E T } } + \sum _ { h \in \mathrm { a u x i l i a r y } } L _ { \mathrm { a u x } , h } ,\tag{53}
$$
<!-- BLOCK_END: b_222 -->

<!-- BLOCK: b_223 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.22. Co-DETR -->
其中LDET是标准DETR损失，$L _ { \mathrm { a u x } , h }$表示每个辅助头的一对多分配损失。
这种混合分配通过增加每批正样本数量改善梯度流动，通过额外反馈信号增强编码器监督，并在COCO和LVIS等基准上获得更好的检测性能。
通过在不改变推理过程的情况下丰富训练监督，Co-DETR实现了更快的收敛、更有效的学习以及基于DETR的目标检测器更高的精度。
<!-- BLOCK_END: b_223 -->

<!-- BLOCK: b_224 | type: figure_caption | heading: Object Detection with Transformers: A Review > 3.22. Co-DETR -->
![](Images_GFP684MN/d02651a8844595ff0e89226c712f509c9644f1df46a487bdd3f97671c2cea1fc.jpg) Figure 10。
添加Co-DETR [37]、RT-DETR和LW-DETR [38]后原始DETR的结构。
此处，网络为简单的DETR网络，改进部分以小彩色方块标示。
浅红色指示块表示Co-DETR，蓝色色块表示LW-DETR，紫色色块表示RT-DETR。
<!-- BLOCK_END: b_224 -->

<!-- BLOCK: b_225 | type: heading | heading: Object Detection with Transformers: A Review > 3.23. LW-DETR -->
## 3.23.
LW-DETR
<!-- BLOCK_END: b_225 -->

<!-- BLOCK: b_226 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.23. LW-DETR -->
LW-DETR [40]是一种轻量级的基于Transformer的目标检测模型，旨在实现高精度和实时性能。
它通过使用优化的视觉Transformer（ViT）编码器和浅层解码器简化了标准DETR架构。
模型首先将输入图像分割为图像块，并通过编码器提取特征。
这些特征随后通过卷积投影层进行细化，然后传入解码器，解码器使用一组目标查询预测边界框和类别标签。
在Figure 10中，蓝色方块表示LW-DETR。
LW-DETR通过多种策略进一步提升效率：交错窗口注意力和全局注意力降低了自注意力的复杂度，多层特征聚合捕获了更丰富的表示，窗口为主的特征图组织优化了注意力计算。
在训练期间，模型采用可变形交叉注意力聚焦于相关区域，IoU感知分类损失增强定位精度，编码器-解码器预训练学习鲁棒特征。
总训练损失结合了分类损失、边界框回归损失和IoU损失以有效指导学习。
<!-- BLOCK_END: b_226 -->

<!-- BLOCK: b_227 | type: equation | heading: Object Detection with Transformers: A Review > 3.23. LW-DETR -->
$$
L _ { \mathrm { t o t a l } } = L _ { \mathrm { c l s } } + L _ { \mathrm { b o x } } + \lambda _ { \mathrm { g i o u } } L _ { \mathrm { G I o U } } ,\tag{54}
$$
<!-- BLOCK_END: b_227 -->

<!-- BLOCK: b_228 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.23. LW-DETR -->
其中$L _ { \mathrm { c l s } }$是分类损失，$L _ { \mathrm { b o x } }$是边界框回归损失，$L _ { \mathrm { G I o U } }$是广义交并比损失，$\lambda _ { \mathrm { g i o u } }$平衡各损失的贡献。
实验结果表明，LW-DETR在保持较低计算成本的同时，实现了比许多实时检测器（包括YOLO变体）更高的精度，适用于实时目标检测任务。
<!-- BLOCK_END: b_228 -->

<!-- BLOCK: b_229 | type: heading | heading: Object Detection with Transformers: A Review > 3.24. RT-DETR -->
## 3.24.
RT-DETR
<!-- BLOCK_END: b_229 -->

<!-- BLOCK: b_230 | type: paragraph | heading: Object Detection with Transformers: A Review > 3.24. RT-DETR -->
RT-DETR [41]（实时检测Transformer）是由百度开发的基于Transformer的目标检测模型，专为适用于实时应用的高速端到端推理而设计。
在Figure 10中，紫色方块表示RT-DETR。
该模型采用混合编码器，通过解耦尺度内交互和跨尺度特征融合来处理多尺度特征。
这种高效设计在保留丰富特征表示的同时降低了计算成本。
编码器输出多尺度特征图，然后传入DETR风格的解码器。
利用IoU感知查询选择机制聚焦于最相关的目标查询，提升检测精度。
此外，推理速度可通过改变解码器层数进行调整，允许在不同实时场景中灵活部署。
后续版本在此基础上进一步提升性能。
RT-DETRv2 [224]引入了选择性多尺度采样，并用离散采样算子替代网格采样算子，改善了对不同尺度目标的检测。
它还采用动态数据增强和尺度自适应超参数调优，在不增加推理延迟的情况下提升训练效率。
RT-DETRv3 [225]通过添加基于CNN的辅助分支实现密集监督、自注意力扰动策略实现多样化标签分配，以及共享权重解码器分支实现密集正样本监督，解决了稀疏监督和解码器训练不足的问题。
总而言之，RT-DETR系列展示了实时目标检测的清晰演进，每个版本都引入了提升速度和精度的架构和训练创新。
原始RT-DETR奠定了实时性能的基础，而v2和v3在不牺牲推理效率的情况下逐步提升了检测能力。
比较检测Transformer中的改进以理解其对网络规模、训练收敛和性能的影响至关重要。
在本工作中，我们使用COCO2014 mini验证集（minival）作为基准，因为COCO是评估目标检测模型的广泛接受标准[75]。
所有图像使用标准调整大小和归一化程序进行预处理，并应用随机水平翻转等数据增强，与典型的DETR训练协议一致。
DETR及其变体的性能使用平均精度均值（mAP）进行评估，其计算方式为每个目标类别的平均精度（AP）的均值，其中AP对应精确率-召回率曲线下面积[226]。
按照标准COCO评估协议，目标根据像素面积分为三个尺寸类别：小目标（$( < 3 2 ^ { 2 }$像素）、中等目标（$( 3 2 ^ { 2 } - 9 6 ^ { 2 }$像素）和大目标（$( > 9 6 ^ { 2 }$像素）。
这种分类允许对不同目标尺度进行详细分析，其中$\mathrm { A P } _ { \mathrm { S } } , \mathrm { A P } _ { \mathrm { M } } .$、$\mathrm { A P _ { L } }$分别报告小目标、中等目标和大目标的性能。
为公平比较，所有结果通过加载各作者发布的原始预训练PTH文件并在COCO minival集上验证获得。
这种方法使我们能够复现各模型的报告性能，同时聚焦于各种DETR变体引入的架构差异和改进。
<!-- BLOCK_END: b_230 -->

<!-- BLOCK: b_233 | type: heading | heading: Object Detection with Transformers: A Review > 4. Results and Discussion -->
## 4.
结果与讨论
<!-- BLOCK_END: b_233 -->

<!-- BLOCK: b_234 | type: paragraph | heading: Object Detection with Transformers: A Review > 4. Results and Discussion -->
DETR中提出了许多改进，如骨干网络修改、查询设计和注意力细化，以提升性能和训练收敛。
Table 3展示了所有基于DETR的检测Transformer在COCO minival集上的性能比较。
我们可以观察到，DETR在500个训练周期时表现良好，但在小目标上的AP较低。
改进版本提升了性能和训练收敛，如DINO在12个周期时mAP达到49.0%，且在小目标上表现良好。
对DETR及其更新版本在COCO minival集上的训练收敛性和模型规模进行了定量分析。
Figure 11左侧展示了使用ResNet-50骨干网络的检测Transformer的mAP随训练周期的变化。
原始DETR以棕色线表示，训练收敛较低。
它在50个训练周期时mAP值为35.3%，在500个训练周期时为44.9 %。
此处，DINO以红色线表示，在较低训练周期时收敛，并在所有周期值上给出最高mAP。
DETR中的注意力机制涉及计算每对特征向量之间的成对注意力分数，计算成本较高，尤其对于大输入图像。
此外，DETR中的自注意力机制依赖使用固定位置编码来编码输入图像不同部分之间的空间关系。
这可能减慢训练过程并增加收敛时间。
相比之下，Deformable-DETR和DINO进行了一些有助于加速训练过程的改进。
例如，Deformable-DETR引入了可变形注意力层，能更好地捕获空间上下文信息并提升目标检测精度。
类似地，DINO使用去噪学习方法训练网络学习对目标检测更有用的泛化特征，使训练过程更快更有效。
Figure 11右侧比较了所有检测Transformer的模型规模。
此处，YOLOS-DETR使用DeiT-small作为骨干网络替代DeiT-Ti，但也使模型规模增加了20倍。
DINO和REGO-DETR具有可比的mAP，但REGO-DETR的模型规模几乎是DINO的两倍。
这些网络使用了比原始DETR架构更复杂的架构，增加了总参数量和整体网络规模。
我们还在Figure 12中提供了DETR及其更新版本在所有尺寸目标上的定性分析。
对于小目标，原始DETR在50个周期时的mAP为15.2%，而Deformable-DETR在50个周期时的mAP值为26.4%。
Deformable-DETR中的自注意力机制使其能够从邻近像素插值特征，这对于可能仅占图像中几个像素的小目标特别有用。
Deformable-DETR中的这种机制捕获了关于小目标更精确和详细的信息，可能带来比DETR更好的性能。
<!-- BLOCK_END: b_234 -->

<!-- BLOCK: b_238 | type: table_caption | heading: Object Detection with Transformers: A Review > 4. Results and Discussion -->
Table 3。
所有基于DETR的检测Transformer在COCO minival集上的性能比较。
此处，标注为DC5的网络采用膨胀特征图。
IoU阈值设置为0.5和0.75用于AP计算，同时计算小目标$( A P _ { s } ) ,$、中等目标$( A P _ { m } ) ,$和大目标（APl）的AP。
+表示边界框细化，++表示Deformable-DETR。
∗∗表示Efficient-DETR使用了6层编码器和1层解码器。
S表示小型，B表示基础型。
†表示Touvron等人的蒸馏机制[227]。
‡表示模型在ImageNet-21k上进行了预训练。
所有模型使用300个查询，而DETR使用100个目标查询输入解码器网络。
带∗上标的模型使用三种模式嵌入。
本表中所有GitHub链接访问于2025年9月25日。
<!-- BLOCK_END: b_238 -->

<!-- BLOCK: b_239 | type: table | heading: Object Detection with Transformers: A Review > 4. Results and Discussion -->
<table><tr><td>方法</td><td>骨干网络</td><td>出版物</td><td>训练周期</td><td>GFLOPs</td><td>参数量 (M)</td><td>AP</td><td> $\mathbf { A } \mathbf { P } ^ { 5 0 }$ </td><td> $\mathbf { A } \mathbf { P } ^ { 7 5 }$ </td><td> $\mathbf { A P _ { S } }$ </td><td> $\mathbf { A P _ { M } }$ </td><td></td><td> $\mathbf { A P _ { L } }$ </td></tr><tr><td rowspan="2">DETR[11]GitHub htps://github.com/facebookresearch/detr</td><td>DC5-ResNet-50 DC5-ResNet-50</td><td rowspan="2">ECCV 2020</td><td>50</td><td>187</td><td>41460</td><td>35.3</td><td>55.7 </td><td>36.8 8</td><td></td><td>15.2</td><td>37.5</td><td>53.6</td></tr><tr><td>DC5-ResNet-101</td><td>500</td><td></td><td></td><td>8</td><td></td><td></td><td></td><td>2</td><td></td><td>611 62.3</td></tr><tr><td rowspan="2">Deformable-DETR [20] GitHub</td><td>ResNet-50</td><td rowspan="2">ICLR 2021</td><td>50</td><td>173</td><td></td><td></td><td>43.8 62.6</td><td>47.7</td><td></td><td>26.4</td><td></td><td>58.0</td></tr><tr><td>ResNet-50 +</td><td>50</td><td>173</td><td>40 40</td><td></td><td>45.4</td><td>64.7</td><td></td><td>26.8</td><td>47.1 48.3</td><td></td></tr><tr><td rowspan="2">https://gitub.com/fundamentalvision/Deformable-DETR</td><td rowspan="2">ResNet-50 ++ ResNet-50</td><td rowspan="2">CVPR 2021</td><td>50</td><td>173</td><td>40</td><td></td><td>65.2</td><td>49.0 50.0</td><td>28.8</td><td></td><td>61.7</td><td></td></tr><tr><td></td><td>86</td><td>41</td><td></td><td>46.2 40.5</td><td>60.8</td><td></td><td>19.0</td><td>49.2 44.4</td><td>61.7</td></tr><tr><td rowspan="2">UP-DETR [21]GitHub htps://github.com/ddzg/up-etr</td><td rowspan="2">ResNet-50 ResNet-50</td><td rowspan="2">arXiv 2021</td><td>150 300</td><td>86</td><td>41</td><td></td><td>42.8 63.0</td><td>42.6 45.3</td><td></td><td>20.8</td><td></td><td>60.0</td></tr><tr><td></td><td>159</td><td>3254</td><td></td><td>44.2</td><td>62.2</td><td>48.0</td><td>28.4</td><td>47.1 47.5</td><td>61.7</td></tr><tr><td rowspan="2">Efficint-DETR [22]</td><td rowspan="2">ResNet-101 ResNet-101 ** ResNet-50</td><td rowspan="2"></td><td>36630</td><td>239</td><td></td><td></td><td>45.2 637</td><td>48.8</td><td></td><td>28.8</td><td>49.1</td><td>56.6 59.0</td></tr><tr><td></td><td>289 152</td><td></td><td>45.7</td><td>64.1</td><td></td><td>49.5</td><td>28.2</td><td>49.1</td><td>60.2</td></tr><tr><td rowspan="2"> SMCA-DETR[23]GitHub htps://github.com/gaopengcuhk/SMCA-DETR</td><td rowspan="2">ResNet-50 ResNet-101</td><td rowspan="2">ICCV 2021</td><td rowspan="2"></td><td>152</td><td></td><td>404058</td><td>4</td><td>63.6 65.5</td><td>47.2</td><td>24.2 25.9</td><td>47.0</td><td>60.4</td></tr><tr><td></td><td>218</td><td></td><td>44.4</td><td>65.2</td><td>49.1 48.0</td><td>24.3</td><td>49.3 48.5</td><td>62.6 610</td></tr><tr><td rowspan="2">TSP-DETR [24]GitHub https://github.com/Edward-Sun/TSP-Detection</td><td rowspan="2">FCOS-ResNet-50 RCNN-ResNet-50</td><td rowspan="2">ICCV 2021</td><td rowspan="2">36</td><td>189</td><td></td><td>51.5</td><td>43.1</td><td>62.3</td><td></td><td>26.6</td><td></td><td></td></tr><tr><td></td><td>188</td><td>63.6</td><td>43.8</td><td>63.3</td><td>47.0 48.3</td><td>28.6</td><td>46.8 46.9</td><td>55.9 55.7</td></tr><tr><td>Conditional-DETR[25]GitHubhtps://github.com/Atten4Vis/ConditionalDETR</td><td>DC5-ResNet-50</td><td>ICCV 2021</td><td>50</td><td>195</td><td>8</td><td></td><td>8 64</td><td>46.7</td><td></td><td>2</td><td>47.6</td><td>60.7</td></tr><tr><td>WB-DETR[26]GitHub https://github.com/aybora/wbdetr</td><td>DC5-ResNet-101 -</td><td>ICCV 2021</td><td>500</td><td>98</td><td>24</td><td></td><td>65.5 41.8 63.2</td><td>48.4 44.8</td><td></td><td>19.4</td><td>48.9</td><td>62.8</td></tr><tr><td>PnP-DETR[27]GitHub htps://github.com/twangh/-det</td><td>DC5-ResNet-50</td><td>ICCV 2021</td><td>500</td><td>145</td><td>41</td><td></td><td>43.1 63.4</td><td>45.3</td><td></td><td>22.7</td><td>45.1 46.5</td><td>62.4 61.1</td></tr><tr><td>Dynamc-DETR [28]</td><td>ResNet-50</td><td>ICCV 2021</td><td>12</td><td>-</td><td>58</td><td></td><td>42.961.0</td><td>46.3</td><td></td><td></td><td>44.9</td><td>54.4</td></tr><tr><td rowspan="2"> YOLOS-DETR [29] GitHub htps://github.com/hustvl/YOLOS</td><td rowspan="2">DeiT-S [227]t DeiT-B[227]t</td><td rowspan="2"></td><td rowspan="2">150</td><td>150</td><td>194</td><td>31</td><td></td><td>56.5</td><td></td><td></td><td></td><td></td></tr><tr><td>NeurIPS 2021</td><td>538</td><td>127</td><td>361</td><td>62.2</td><td>37.1 44.5</td><td>15.3</td><td>38.5</td><td>56.2</td></tr><tr><td> Anchor-DETR[30]GitHub https://github.com/megvi-esearch/AnchorDETR</td><td>DC5-ResNet-50 *</td><td>AAAI 2022</td><td>5</td><td>151</td><td>38</td><td></td><td>44.2 647</td><td>47.5</td><td></td><td>19.5 24.7</td><td>45.3 48.2</td><td>62.1 60.6</td></tr><tr><td> Sparse-DETR[31]GitHub htps://github.com/kakaobrain/sparse-detr</td><td>DC5-ResNet-101 * ResNet-50-p-0.5</td><td>ICLR 2022</td><td>50</td><td>237 16</td><td></td><td></td><td>45.1 46.3</td><td>65.7 48.8 50.1</td><td></td><td>25.8 29.0</td><td>49. 49.5</td><td>61.6 60.8</td></tr><tr><td rowspan="2">D2ETR[32]GitHubhttps://github.com/alibab/easyrobust/tree/mainddetr Def D2ETR[32]</td><td rowspan="2">Swin-T-p-0.5[228] PVT2 PVT2</td><td rowspan="2">arXiv 2022</td><td rowspan="2">50</td><td rowspan="2"></td><td></td><td></td><td>49.3</td><td>66.0 69.5</td><td></td><td></td><td></td><td></td></tr><tr><td></td><td>4 8 3</td><td>43.2 50.0 67.9</td><td>62.9</td><td>53.3 46.2</td><td>32.0 22.0</td><td>52.7 48.5</td><td>64.9</td></tr></table>
Table 3。
续
<!-- BLOCK_END: b_239 -->

<!-- BLOCK: b_240 | type: table | heading: Object Detection with Transformers: A Review > 4. Results and Discussion -->
<table><tr><td>方法</td><td>骨干网络</td><td>发表</td><td>训练轮次 50550</td><td>GFLOPs</td><td>参数量 (M)</td><td>AP</td><td>AP50</td><td> $\mathbf { A } \mathbf { P } ^ { 7 5 }$ </td><td>APs</td><td> $\mathbf { A P _ { M } }$ </td><td>APL</td></tr><tr><td rowspan="2">FP-DETR-S[3GitHubhtts://github.com/encounter197/F-DER FP-DETR-B3]GitHubhps://githubcom/encounter1997/F-D</td><td>- -</td><td rowspan="2">ICLR 2022</td><td></td><td>102</td><td></td><td>42.5 43.3</td><td>62.6</td><td>45.9 47.7</td><td>25.3 27.5</td><td>45.5 46.1</td><td>56.9</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td>63.9</td><td></td><td></td><td></td><td>57.0</td></tr><tr><td rowspan="2">FP-DETR-B‡33]GitHubhps://githubom/encounter1997/F-DT CF-DETR [34]</td><td>-</td><td rowspan="2"></td><td>36</td><td>1</td><td>243630</td><td>43.7</td><td>641</td><td>47.8</td><td>26.5</td><td>46.7</td><td>58.2</td></tr><tr><td>ResNet-50</td><td></td><td></td><td></td><td>47.8</td><td>66.5</td><td>52.4</td><td>31.2</td><td>50.6 52.2</td><td>62.8</td></tr><tr><td rowspan="2"> DAB-DETR [72] GitHub https://github.com/IDEA-Research/DAB-DETR</td><td>ResNet-101</td><td rowspan="2">AAAI 2022 ICLR 2022</td><td></td><td>--</td><td>-</td><td>49.0</td><td>68.1</td><td>53.4</td><td>314</td><td></td><td>64.3</td></tr><tr><td>DC5-ResNet-50 * DC5-ResNet-101 *</td><td></td><td>216</td><td>44</td><td>45.7</td><td>66.2</td><td>49.0</td><td>26.1</td><td>49.4</td><td>63.1</td></tr><tr><td rowspan="2"></td><td></td><td rowspan="2"></td><td>50</td><td>296</td><td>63</td><td>46.6</td><td>67.0</td><td>50.2</td><td>28.1</td><td>50.5</td><td>64.1</td></tr><tr><td>ResNet-50 DC5-ResNet-50</td><td>5050</td><td>94 202</td><td></td><td>44.1</td><td>64.4</td><td>46.7 49.7</td><td>22.9 26.7</td><td>48.0</td><td>63.4</td></tr><tr><td rowspan="2"> DN-DETR [35] GitHub https://github.com/IDEA-Research/DN-DETR</td><td>ResNet-101</td><td rowspan="2">CVPR 2022</td><td></td><td>174</td><td>4466</td><td>46.3 45.2</td><td>66.4 65.5</td><td>48.3</td><td>24.1</td><td>50.0</td><td>64.3</td></tr><tr><td>DC5-ResNet-101</td><td></td><td></td><td></td><td>47.3</td><td>67.5</td><td>50.8</td><td>28.6</td><td>49.1 51.5</td><td>65.1 65.0</td></tr><tr><td rowspan="2"> AdaMixer [36]GitHub htps://github.com/MCG-NJU/AdaMixer</td><td>ResNet-50</td><td rowspan="2">CVPR 2022</td><td></td><td>132</td><td>10</td><td></td><td>66.0</td><td></td><td>30.1</td><td></td><td></td></tr><tr><td>ResNeXt-101-DCN</td><td>33</td><td></td><td></td><td>47.0 49.5</td><td>68.9</td><td>51.1 53.9</td><td>31.3</td><td>50.2 52.3</td><td>61.8 66.3</td></tr><tr><td rowspan="2"></td><td>Swin-s [228]</td><td rowspan="2"></td><td></td><td>2</td><td>164</td><td>51.3</td><td>712</td><td>55.7</td><td>34.2</td><td></td><td></td></tr><tr><td>ResNet-50 ++</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>54.6</td><td>67.3</td></tr><tr><td rowspan="2">REGO [37] GitHub htps://github.com/zhechen/Deformable-DETR-REGO</td><td>ResNet-101 ++</td><td rowspan="2">CVPR 2022</td><td></td><td>190 23</td><td></td><td>47.6 48.5</td><td>66.8 67.0</td><td>51.6 52.4</td><td>29.6 29.5</td><td>50.6</td><td>62.3</td></tr><tr><td>ReNeXt-101 ++</td><td>50550</td><td></td><td></td><td>49.1</td><td>67.5</td><td>53.1</td><td>30.0</td><td>52.0 52.6</td><td>644 65.0</td></tr><tr><td rowspan="2">DINO [38] GitHub htps://github.com/facebookresearch/dino</td><td>ReNet-50-4scale *</td><td rowspan="2"></td><td></td><td>279</td><td>5万</td><td></td><td></td><td>53.5</td><td>32.0</td><td></td><td></td></tr><tr><td>ResNet-50-5scale *</td><td>12</td><td>860</td><td></td><td>49.0 49.4</td><td>66.6 66.9</td><td>53.8</td><td>32.3</td><td>52.3 52.5</td><td>63.0 63.9</td></tr><tr><td rowspan="2"></td><td>ReNet-50-5scale *</td><td rowspan="2">arXiv 2022</td><td>24</td><td>860</td><td>4 47</td><td>51.3</td><td>69.1</td><td>56.0</td><td>34.5</td><td></td><td></td></tr><tr><td>ResNet-50-5scale *</td><td>36</td><td>860</td><td></td><td>51.2</td><td>69.0</td><td>55.8</td><td>35.0</td><td>54.2 54.3</td><td>65.8</td></tr><tr><td rowspan="2">Co-DETR [39]GitHub htps://github.com/Sense-X/Co-DETR</td><td>ReNet-50 *</td><td rowspan="2"></td><td></td><td>279</td><td>47</td><td>52.1</td><td>69.3</td><td>57.3</td><td>35.4</td><td></td><td>65.3</td></tr><tr><td>ReNet-50 *</td><td>136122</td><td>860</td><td></td><td>54.8</td><td>72.5</td><td>60.1</td><td>38.3</td><td>55.5 58.4</td><td>67.2</td></tr><tr><td rowspan="2"></td><td>Swin-L(IN-22K) *</td><td rowspan="2">ICCV 2023</td><td></td><td>860</td><td>老 47</td><td>59.3</td><td>77.3</td><td>64.9</td><td>43.3</td><td></td><td>69.6</td></tr><tr><td>Swin-L(IN-22K) *</td><td>34</td><td>860</td><td></td><td>60.4</td><td>78.3</td><td>66.4</td><td>44.6</td><td>63.3 64.2</td><td>75.5 76.5</td></tr><tr><td rowspan="2"> LW-DETR [40] GitHub https://github.com/Atten4Vis/LW-DETR</td><td>Swin-L(IN-22K) *</td><td rowspan="2">arXiv 2024</td><td></td><td>860</td><td>老</td><td>60.7</td><td>785</td><td>66.7</td><td>45.1</td><td>64.7</td><td>76.</td></tr><tr><td>-</td><td>50</td><td>67.7</td><td>54.6</td><td>54.4</td><td>1</td><td>-</td><td>48.0</td><td>52.5</td><td>56.1</td></tr><tr><td> RT-DETR [41] GitHub https://github.com/lyuwenyu/RT-DETR</td><td>ReNet-50*</td><td>CVPR 2024</td><td></td><td>136</td><td>42</td><td>53.1</td><td>71.3</td><td>57.7</td><td>34.8</td><td>58.0</td><td>70.0</td></tr><tr><td rowspan="2">RT-DETRv2 [24]GitHub htps:/ /github.com/supervisely-cosystem/RT-DETRv2</td><td>ResNet-101 *</td><td></td><td>2</td><td>259</td><td>76</td><td>54.3</td><td>72.7</td><td>58.6</td><td>36.0</td><td>58.8</td><td>72.1</td></tr><tr><td>ReNet-50 * ResNet-101 *</td><td>arXiv 2024</td><td>2</td><td></td><td></td><td>53.4</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td> RT-DETRv3[25]GitHub htps://github.com/cxia12/RT-DETRv3</td><td>ReNet-50*</td><td>arXiv 2024</td><td>2</td><td>13 136</td><td>5</td><td>543 53.4</td><td></td><td></td><td></td><td>-</td><td></td></tr></table>
![](Images_GFP684MN/507382105aa07b518da378c858c0804b145742c736532e299fb2a7515008dafd.jpg) Figure 11.
在 COCO minival 集合上对所有基于 DETR 的检测 Transformer 进行比较。左图：使用 ResNet-50 [80] 骨干网络的检测 Transformer 在不同训练轮次下的性能比较。
标注为 DC5 的网络采用空洞特征图。右图：检测 Transformer 在模型规模（参数量，单位：百万）方面的性能比较。
![](Images_GFP684MN/7fdef3c2e7ca24ac1bb08ff3235b30a4014b6b82370b4f86d54f05e46edbc78d.jpg) Figure 12.
在 COCO minival 集合上使用 ResNet-50 骨干网络对基于 DETR 的检测 Transformer 进行比较。左图：检测 Transformer 在小目标上的性能比较。中图：检测 Transformer 在中等目标上的性能比较。右图：检测 Transformer 在大目标上的性能比较。
尽管 DINO 展现了令人瞩目的精度和快速收敛能力，但其计算开销仍然是一个重大问题。
DINO 每次推理约需 5–10 GFLOPs，远比 Nano YOLO 变体等轻量级替代方案的计算需求更高，后者通常在 5–10 GFLOPs 范围内运行。
这一显著差异凸显了许多基于 DETR 模型的一个根本性局限：尽管精度有所提升，但其推理成本使其不适用于对延迟敏感或资源受限的应用场景。
相比之下，RT-DETR 和 LW-DETR 提供了轻量级和实时的 DETR 变体，以显著更低的计算负荷实现了有竞争力的精度（RT-DETR 为 136–259 GFLOPs，LW-DETR 为 67.7 GFLOPs）。
此外，Co-DETR 专注于增强上下文推理以进一步提升检测性能，取得了非常高的 AP 分数，但其计算成本与 DINO 相当，同样较高。
因此，未来的研究不仅需要解决精度和收敛速度问题，还需要弥合 DETR 变体与轻量级基于 CNN 检测器之间的效率差距，以确保其在实际场景中的实际适用性。
虽然 Table 3 和图 11、图 12 展示了性能改进，但同样需要考虑计算成本、内存占用和实现复杂度。
诸如 DINO 和 REGO 等模型虽然取得了高 mAP，但需要显著更多的参数和 GFLOPs，使其不太适合资源受限的场景。
Deformable-DETR 通过在不大幅增加计算负荷的情况下改进小目标检测和收敛速度，提供了均衡的折中方案。
YOLOS-DETR 虽然设计紧凑，但依赖于 DeiT-S Transformer 骨干网络，使内存需求增加了高达 20 倍，凸显了模型规模与检测速度之间的折中。
因此，选择 DETR 变体不仅取决于精度，还取决于硬件约束、数据集特性和实时性要求。
<!-- BLOCK_END: b_240 -->

<!-- BLOCK: b_241 | type: heading | heading: Object Detection with Transformers: A Review > 5. Open Challenges and Future Directions -->
## 5.
开放挑战与未来方向
<!-- BLOCK_END: b_241 -->

<!-- BLOCK: b_242 | type: paragraph | heading: Object Detection with Transformers: A Review > 5. Open Challenges and Future Directions -->
检测 Transformer 在多种目标检测基准上展现了令人瞩目的结果。
然而，仍存在若干开放性挑战，为未来的改进提供了方向。
Table 4 总结了 DETR 各种改进版本的优势与局限性。
一些关键的开放性挑战与未来方向如下。
改进注意力机制：检测 Transformer 的性能高度依赖于注意力机制来捕捉图像中空间位置之间的依赖关系。
迄今为止，DETR 中约 60% 的改进集中于注意力机制，以提升性能和训练收敛速度。
未来研究可以探索更精细的注意力机制，以更好地捕捉空间信息或融入任务特定的约束。
自适应和动态骨干网络：骨干网络架构显著影响网络性能和模型规模。
当前的检测 Transformer 通常采用固定的骨干网络或完全去除骨干网络。
仅有约 10% 的 DETR 改进针对骨干网络以提升性能或减小模型规模。
未来工作可以研究动态骨干网络架构，根据输入图像调整其复杂度，从而有望同时提升效率和精度。
提高目标查询的数量和质量：在 DETR 中，输入解码器的目标查询数量在训练和推理期间通常是固定的，但图像中的目标数量是变化的。
后续方法，如 DAB-DETR、DN-DETR 和 DINO，表明调整目标查询的数量或质量可以显著影响性能。
DAB-DETR 使用动态锚框作为查询，DN-DETR 向查询添加正噪声用于去噪训练，DINO 同时添加正噪声和负噪声以改进去噪效果。
未来模型可以根据图像内容动态调整目标查询数量，并融入自适应机制以提高查询质量。
新兴方向：除注意力机制、骨干网络和目标查询之外，仍存在若干额外挑战。
通过更快的收敛策略和样本高效学习来提高训练效率，可以使 DETR 更适用于大规模应用。
整合多任务学习，如联合执行检测、分割和跟踪，可以利用共享表征获得更好的性能。
增强在遮挡、域偏移或低分辨率输入条件下的鲁棒性和泛化能力同样至关重要。
跨学科方法可以融入强化学习来引导模型自适应、采用 NLP 启发的序列建模来改善特征交互，或利用基于图的推理技术来捕捉目标之间的关系。
具体的研究挑战包括设计能够动态适应新任务或新域的模型，以及开发整合多种数据源以实现更丰富场景理解的跨模态注意力机制。
<!-- BLOCK_END: b_242 -->

<!-- BLOCK: b_247 | type: table_caption | heading: Object Detection with Transformers: A Review > 5. Open Challenges and Future Directions -->
Table 4。
检测 Transformer 的优势与局限性概述。
本表中所有 GitHub 链接的访问日期为 2025 年 9 月 25 日。
<!-- BLOCK_END: b_247 -->

<!-- BLOCK: b_248 | type: table | heading: Object Detection with Transformers: A Review > 5. Open Challenges and Future Directions -->
<table><tr><td>方法</td><td>发表</td><td>优势</td><td>局限性</td></tr><tr><td>DETR [11] GitHub https://github.com/facebookresearch/detr</td><td>ECCV 2020</td><td>消除了 NMS 或锚框生成等手工设计组件的需求。</td><td>在小目标上性能较低，训练收敛缓慢。</td></tr><tr><td>Deformable-DETR [20] GitHub https://github.com/fundamentalvision/D eformable-DETR</td><td>ICLR 2021</td><td>可变形注意力网络，与 DETR 相比使训练收敛更快。</td><td>编码器令牌数量增加 20 倍</td></tr></table>
Table 4。
续。
<!-- BLOCK_END: b_248 -->

<!-- BLOCK: b_249 | type: table | heading: Object Detection with Transformers: A Review > 5. Open Challenges and Future Directions -->
<table><tr><td>方法</td><td>发表</td><td>优势</td><td>局限性</td></tr><tr><td>UP-DETR [21] GitHub https://github.com/dddzg/up-detr</td><td>CVPR 2021</td><td>用于多任务学习和多查询定位的预训练。</td><td>用于块定位的预训练，CNN 和 Transformer 预训练需要整合。</td></tr><tr><td>Efficient-DETR [22]</td><td>arXiv 2021</td><td>通过采用基于密集和稀疏集合的网络减少解码器层数</td><td>与原始 DETR 相比 GFLOPs 增加两倍。</td></tr><tr><td>SMCA-DETR [23] GitHub https: //github.com/gaopengcuhk/SMCA-DETR</td><td>ICCV 2021</td><td>回归感知机制以提高收敛速度</td><td>小目标检测性能较低。</td></tr><tr><td>TSP-DETR [24] GitHub https: / /github.com/Edward-Sun/TSP-Detection</td><td>ICCV 2021</td><td>解决匈牙利损失和 Transformer 的交叉注意力机制问题。</td><td>使用 TSP-FCOS 中的提议和 TSP-RCNN 中的特征点，如同基于 CNN 的检测器。</td></tr><tr><td>Conditional-DETR [25]GitHub https://gith ub.com/Atten4Vis/ConditionalDETR</td><td>ICCV 2021</td><td>条件查询消除对内容嵌入的依赖并简化训练。</td><td>对于更强的骨干网络，性能优于 DETR 和 deformable-DETR。</td></tr><tr><td>WB-DETR [26] GitHub https://github.com/aybora/wbdetr</td><td>ICCV 2021</td><td>无骨干网络的纯 Transformer 网络。</td><td>在小目标上性能较低。</td></tr><tr><td>PnP-DETR [27] GitHub https://github.com/twangnh/pnp-detr</td><td>ICCV 2021</td><td>采样模块提供前景和少量背景特征。</td><td>通过提取前景令牌和减少背景令牌破坏了二维空间结构。</td></tr><tr><td>Dynamic-DETR [28]</td><td>ICCV 2021</td><td>动态注意力提供较小的特征分辨率并改善训练收敛。</td><td>仍然依赖 CNN 网络作为基于卷积的编码器和基于 RoI 的解码器。</td></tr><tr><td>YOLOS-DETR [29] GitHub https://github.com/hustvl/YOLOS</td><td>NeurIPS 2021</td><td>将在 ImageNet-1k 数据集上预训练的 ViT 转化为目标检测器。</td><td>预训练的 ViT 仍需改进，因为它需要较长的训练轮次。</td></tr><tr><td>Anchor-DETR [30] GitHub htps://github.c om/megvii-research/AnchorDETR</td><td>AAAI 2022</td><td>目标查询作为锚点，在一个位置预测多个目标。</td><td>将查询视为二维锚点，忽略了目标尺度。</td></tr><tr><td>Spare-DETR [31] GitHub https: //github.com/kakaobrain/sparse-detr</td><td>ICLR 2022</td><td>通过更新解码器引用的令牌来提升性能。</td><td>性能强烈依赖于骨干网络，尤其对大目标。</td></tr><tr><td>D²ETR [32] GitHub https://github.com/ali baba/easyrobust/tree/main/ddetr</td><td>arXiv 2022</td><td>仅解码器 Transformer 网络以降低计算成本。</td><td>显著降低了计算复杂度，但在小目标上性能较低。</td></tr><tr><td>FP-DETR [33] GitHub https: // github.com/encounter1997/FP-DETR</td><td>ICLR 2022</td><td>仅编码器 Transformer 的预训练。</td><td>在大目标上性能较低。</td></tr><tr><td>CF-DETR [34] GitHub https://github.com/facebookresearch/detr</td><td>AAAI 2022</td><td>细化粗粒度特征以提高小目标的定位精度。</td><td>新增三个模块增加了网络规模。</td></tr><tr><td>DAB-DETR [72] GitHub https: // github.com/IDEA-Research/DAB-DETR</td><td>ICLR 2022</td><td>锚框作为查询，针对不同尺度目标的注意力。</td><td>仅为前景目标提供位置先验。</td></tr></table>
Table 4。
续。
<!-- BLOCK_END: b_249 -->

<!-- BLOCK: b_250 | type: table | heading: Object Detection with Transformers: A Review > 5. Open Challenges and Future Directions -->
<table><tr><td>方法</td><td>发表</td><td>优势</td><td>局限性</td></tr><tr><td>DN-DETR [35] GitHub https: / / github.com/IDEA-Research/DN-DETR</td><td>CVPR 2022</td><td>对前景和背景区域的位置先验进行去噪训练。</td><td>通过向目标查询添加正噪声进行去噪训练，忽略了背景区域。</td></tr><tr><td>AdaMixer [36] GitHub https://github.com/MCG-NJU/AdaMixer</td><td>CVPR 2022</td><td>更快的收敛，提高基于查询的解码机制的适应性。</td><td>参数量大。</td></tr><tr><td>REGO [37] GitHub https://github.com/zhe chen/Deformable-DETR-REGO</td><td>CVPR 2022</td><td>注意力机制逐渐更精确地聚焦于前景区域。</td><td>多阶段基于 RoI 的注意力建模增加了参数量。</td></tr><tr><td>DINO [38] GitHub https: / /github.com/facebookresearch/dino</td><td>arXiv 2022</td><td>在中小规模数据集上取得令人瞩目的结果</td><td>对大尺寸目标的性能下降</td></tr><tr><td>Co-DETR [39] GitHub https://github.com/Sense-X/Co-DETR</td><td>ICCV 2023</td><td>通过协作混合分配增强编码器特征学习和解码器注意力。</td><td>由于多个分配头增加了训练复杂度。</td></tr><tr><td>LW-DETR [40] GitHub https:/ /github.com/Atten4Vis/LW-DETR</td><td>arXiv 2024</td><td>通过优化的 ViT 编码器和窗口注意力的轻量级 Transformer 设计实现实时检测。</td><td>在基准上的评估有限；不如 YOLO 系列检测器成熟。</td></tr></table>
<!-- BLOCK_END: b_250 -->

<!-- BLOCK: b_251 | type: heading | heading: Object Detection with Transformers: A Review > 6. Conclusions -->
## 6.
结论
<!-- BLOCK_END: b_251 -->

<!-- BLOCK: b_252 | type: paragraph | heading: Object Detection with Transformers: A Review > 6. Conclusions -->
检测 Transformer 通过实现完全端到端的模型，消除了对提议生成和复杂后处理的需求，同时为深度神经网络的内部工作机制提供了洞察，从而变革了目标检测领域。
本综述详细概述了 DETR 及其变体，重点关注旨在提升性能和训练收敛速度的最新进展。
特别是，编码器-解码器网络中注意力模块的改进和目标查询的更新增强了训练稳定性和性能，尤其对小目标效果显著。
其他改进包括骨干网络优化、查询设计增强和注意力机制优化，所有这些都促进了精度和效率的提升。
从本综述中可以归纳出几个高层趋势。
收敛缓慢和小目标检测能力有限仍然是核心挑战，推动着注意力机制、查询设计和骨干网络架构方面的创新。
在 DETR 变体中，共同点包括使用基于 Transformer 的注意力、模块化编码器-解码器设计以及增加正监督的策略，而差异则体现在变体如何平衡精度与效率、实现多尺度特征融合以及分配目标查询等方面。
研究沿两条主要路径分化：以精度为导向的方法利用更深的骨干网络和广泛的预训练，而以效率为导向的方法采用轻量级、稀疏或可变形架构，如 RT-DETR 和 LW-DETR，以较低的计算成本实现有竞争力的性能。
最新趋势进一步强调效率、多任务学习和跨模态整合，实现了更快的收敛、更好的泛化以及更广泛的场景理解，涵盖检测、分割、跟踪和视觉-语言推理。
本综述的关键洞察表明，模型设计越来越受到实时部署与高精度之间折中的塑造，而模块化、自适应架构是实现这一平衡的核心。
总体而言，DETR 已发展为一个模块化且灵活的框架，能够在精度和效率之间取得平衡。
未来方向指向根据输入复杂度动态分配计算资源的自适应架构、面向挑战性环境的鲁棒训练策略，以及通过多模态整合实现更丰富的上下文推理。
通过将架构创新与实际部署考量相结合，Transformer 有望推动下一代可扩展、智能且多功能的视觉感知系统的发展。
作者贡献：撰写、审阅和编辑，T.S.；审阅，K.A.H. 和 M.Z.A.；监督与项目管理，M.L. 和 D.S. 所有作者均已阅读并同意手稿的出版版本。
资助：本工作部分由欧洲项目 AIRISE 资助，资助协议编号 101092312。
致谢：本文收录的所有人员均已同意致谢。
利益冲突：作者声明不存在利益冲突。
<!-- BLOCK_END: b_252 -->

<!-- BLOCK: b_258 | type: heading | heading: Object Detection with Transformers: A Review > References -->
## References
<!-- BLOCK_END: b_258 -->

<!-- BLOCK: b_259 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
1. Ren, S.; He, K.; Girshick, R.B.; Sun, J. Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks. arXiv 2015, arXiv:1506.01497. [CrossRef]
<!-- BLOCK_END: b_259 -->

<!-- BLOCK: b_260 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
2. Girshick, R.B. Fast R-CNN. arXiv 2015, arXiv:1504.08083. [CrossRef]
<!-- BLOCK_END: b_260 -->

<!-- BLOCK: b_261 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
3. Redmon, J.; Farhadi, A. YOLOv3: An Incremental Improvement. arXiv 2018, arXiv:1804.02767. [CrossRef]
<!-- BLOCK_END: b_261 -->

<!-- BLOCK: b_262 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
4. Lin, T.; Goyal, P.; Girshick, R.B.; He, K.; Dollár, P. Focal Loss for Dense Object Detection. arXiv 2017, arXiv:1708.02002.
<!-- BLOCK_END: b_262 -->

<!-- BLOCK: b_263 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
5. Shehzadi, T.; Majid, A.; Hameed, M.; Farooq, A.; Yousaf, A. Intelligent predictor using cancer-related biologically information extraction from cancer transcriptomes. In Proceedings of the 2020 International Symposium on Recent Advances in Electrical Engineering & Computer Sciences (RAEE & CS), Islamabad, Pakistan, 20–22 October 2020; Volume 5, pp. 1–5. [CrossRef]
<!-- BLOCK_END: b_263 -->

<!-- BLOCK: b_264 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
6. Sarode, S.; Khan, M.S.U.; Shehzadi, T.; Stricker, D.; Afzal, M.Z. Classroom-Inspired Multi-mentor Distillation with Adaptive Learning Strategies. In Proceedings of the Intelligent Systems and Applications, Amsterdam, The Netherlands, 27–28 August 2025; Arai, K., Ed.; Springer Nature: Cham, Switzerland, 2025; pp. 294–324. [CrossRef]
<!-- BLOCK_END: b_264 -->

<!-- BLOCK: b_265 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
7. Girshick, R.B.; Donahue, J.; Darrell, T.; Malik, J. Rich feature hierarchies for accurate object detection and semantic segmentation. arXiv 2013, arXiv:1311.2524.
<!-- BLOCK_END: b_265 -->

<!-- BLOCK: b_266 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
8. Dosovitskiy, A.; Beyer, L.; Kolesnikov, A.; Weissenborn, D.; Zhai, X.; Unterthiner, T.; Dehghani, M.; Minderer, M.; Heigold, G.; Gelly, S.; et al. An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale. arXiv 2020, arXiv:2010.11929.
<!-- BLOCK_END: b_266 -->

<!-- BLOCK: b_267 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
9. Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A.N.; Kaiser, L.; Polosukhin, I. Attention is all you need. In Proceedings of the 31st International Conference on Neural Information Processing Systems, Long Beach, CA, USA, 4–9 December 2017; Curran Associates Inc.: Red Hook, NY, USA, 2017; pp. 6000–6010. Available online: https: //dl.acm.org/doi/10.5555/3295222.3295349 (accessed on 25 September 2025).
<!-- BLOCK_END: b_267 -->

<!-- BLOCK: b_268 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
10. Khan, M.S.U.; Shehzadi, T.; Noor, R.; Stricker, D.; Afzal, M.Z. Enhanced Bank Check Security: Introducing a Novel Dataset and Transformer-Based Approach for Detection and Verification. arXiv 2024, arXiv:2406.14370. [CrossRef]
<!-- BLOCK_END: b_268 -->

<!-- BLOCK: b_269 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
11. Carion, N.; Massa, F.; Synnaeve, G.; Usunier, N.; Kirillov, A.; Zagoruyko, S. End-to-End Object Detection with Transformers. In Proceedings of the Computer Vision–ECCV 2020, Glasgow, UK, 23–28 August 2020; Vedaldi, A., Bischof, H., Brox, T., Frahm, J.M., Eds.; Springer International Publishing: Cham, Switzerland, 2020; pp. 213–229. [CrossRef]
<!-- BLOCK_END: b_269 -->

<!-- BLOCK: b_270 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
12. Shehzadi, T.; Hashmi, K.A.; Stricker, D.; Afzal, M.Z. Object Detection with Transformers: A Review. arXiv 2023, arXiv:2306.04670. [CrossRef]
<!-- BLOCK_END: b_270 -->

<!-- BLOCK: b_271 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
13. Sheikh, T.U.; Shehzadi, T.; Hashmi, K.A.; Stricker, D.; Afzal, M.Z. UnSupDLA: Towards Unsupervised Document Layout Analysis. arXiv 2024, arXiv:2406.06236.
<!-- BLOCK_END: b_271 -->

<!-- BLOCK: b_272 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
14. Ehsan, I.; Shehzadi, T.; Stricker, D.; Afzal, M.Z. End-to-End Semi-Supervised approach with Modulated Object Queries for Table Detection in Documents. Int. J. Document Anal. Recognit. 2024, 27, 363–378. Available online: https://api.semanticscholar.org/Co rpusID:269626070 (accessed on on 25 September 2025). [CrossRef]
<!-- BLOCK_END: b_272 -->

<!-- BLOCK: b_273 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
15. Shehzadi, T.; Stricker, D.; Afzal, M.Z. A Hybrid Approach for Document Layout Analysis in Document images. arXiv 2024, arXiv:2404.17888. [CrossRef]
<!-- BLOCK_END: b_273 -->

<!-- BLOCK: b_274 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
16. Shehzadi, T.; Sarode, S.; Stricker, D.; Afzal, M.Z. Towards End-to-End Semi-Supervised Table Detection with Semantic Aligned Matching Transformer. arXiv 2024, arXiv:2405.00187.
<!-- BLOCK_END: b_274 -->

<!-- BLOCK: b_275 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
17. Saeed, W.; Saleh, M.S.; Gull, M.N.; Raza, H.; Saeed, R.; Shehzadi, T. Geometric features and traffic dynamic analysis on 4-leg intersections. Int. Rev. Appl. Sci. Eng. 2024, 15, 171–188. [CrossRef]
<!-- BLOCK_END: b_275 -->

<!-- BLOCK: b_276 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
18. Shehzadi, T.; Hashmi, K.A.; Stricker, D.; Liwicki, M.; Afzal, M.Z. Bridging the Performance Gap between DETR and R-CNN for Graphical Object Detection in Document Images. arXiv 2023, arXiv:2306.13526. [CrossRef]
<!-- BLOCK_END: b_276 -->

<!-- BLOCK: b_277 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
19. Shehzadi, T.; Hashmi, K.A.; Stricker, D.; Afzal, M.Z. Sparse Semi-DETR: Sparse Learnable Queries for Semi-Supervised Object Detection. arXiv 2024, arXiv:2404.01819.
<!-- BLOCK_END: b_277 -->

<!-- BLOCK: b_278 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
20. Zhu, X.; Su, W.; Lu, L.; Li, B.; Wang, X.; Dai, J. Deformable DETR: Deformable Transformers for End-to-End Object Detection. arXiv 2020, arXiv:2010.04159.
<!-- BLOCK_END: b_278 -->

<!-- BLOCK: b_279 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
21. Dai, Z.; Cai, B.; Lin, Y.; Chen, J. UP-DETR: Unsupervised Pre-training for Object Detection with Transformers. arXiv 2020, arXiv:2011.09094.
<!-- BLOCK_END: b_279 -->

<!-- BLOCK: b_280 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
22. Yao, Z.; Ai, J.; Li, B.; Zhang, C. Efficient DETR: Improving End-to-End Object Detector with Dense Prior. arXiv 2021, arXiv:2104.01318.
<!-- BLOCK_END: b_280 -->

<!-- BLOCK: b_281 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
23. Gao, P.; Zheng, M.; Wang, X.; Dai, J.; Li, H. Fast Convergence of DETR with Spatially Modulated Co-Attention. arXiv 2021, arXiv:2101.07448.
<!-- BLOCK_END: b_281 -->

<!-- BLOCK: b_282 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
24. Sun, Z.; Cao, S.; Yang, Y.; Kitani, K. Rethinking Transformer-based Set Prediction for Object Detection. arXiv 2020, arXiv:2011.10881.
<!-- BLOCK_END: b_282 -->

<!-- BLOCK: b_283 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
25. Meng, D.; Chen, X.; Fan, Z.; Zeng, G.; Li, H.; Yuan, Y.; Sun, L.; Wang, J. Conditional DETR for Fast Training Convergence. arXiv 2021, arXiv:2108.06152.
<!-- BLOCK_END: b_283 -->

<!-- BLOCK: b_284 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
26. Liu, F.; Wei, H.; Zhao, W.; Li, G.; Peng, J.; Li, Z. WB-DETR: Transformer-Based Detector without Backbone. In Proceedings of the 2021 IEEE/CVF International Conference on Computer Vision (ICCV), Montreal, QC, Canada, 11–17 October 2021; pp. 2959–2967. [CrossRef]
<!-- BLOCK_END: b_284 -->

<!-- BLOCK: b_285 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
27. Wang, T.; Yuan, L.; Chen, Y.; Feng, J.; Yan, S. PnP-DETR: Towards Efficient Visual Analysis with Transformers. arXiv 2021, arXiv:2109.07036.
<!-- BLOCK_END: b_285 -->

<!-- BLOCK: b_286 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
28. Dai, X.; Chen, Y.; Yang, J.; Zhang, P.; Yuan, L.; Zhang, L. Dynamic DETR: End-to-End Object Detection with Dynamic Attention. In Proceedings of the 2021 International Conference on Computer Vision, Montreal, QC, Canada, 11–17 October 2021. Available online: https://www.microsoft.com/en-us/research/publication/dynamic-detr-end-to-end-object-detection-with-dynamic -attention/ (accessed on 25 September 2025).
<!-- BLOCK_END: b_286 -->

<!-- BLOCK: b_287 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
29. Fang, Y.; Liao, B.; Wang, X.; Fang, J.; Qi, J.; Wu, R.; Niu, J.; Liu, W. You Only Look at One Sequence: Rethinking Transformer in Vision through Object Detection. arXiv 2021, arXiv:2106.00666. [CrossRef]
<!-- BLOCK_END: b_287 -->

<!-- BLOCK: b_288 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
30. Wang, Y.; Zhang, X.; Yang, T.; Sun, J. Anchor DETR: Query Design for Transformer-Based Detector. In Proceedings of the AAAI Conference on Artificial Intelligence, Online, 22 February–1 March 2022. Available online: https://api.semanticscholar.org/Corp usID:237513850 (accessed on 25 September 2025).
<!-- BLOCK_END: b_288 -->

<!-- BLOCK: b_289 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
31. Roh, B.; Shin, J.; Shin, W.; Kim, S. Sparse DETR: Efficient End-to-End Object Detection with Learnable Sparsity. arXiv 2021, arXiv:2111.14330.
<!-- BLOCK_END: b_289 -->

<!-- BLOCK: b_290 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
32. Lin, J.; Mao, X.; Chen, Y.; Xu, L.; He, Y.; Xue, H. D2ETR: Decoder-Only DETR with Computationally Efficient Cross-Scale Attention. arXiv 2022, arXiv:2203.00860. [CrossRef]
<!-- BLOCK_END: b_290 -->

<!-- BLOCK: b_291 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
33. Wang, W.; Cao, Y.; Zhang, J.; Tao, D. FP-DETR: Detection Transformer Advanced by Fully Pre-training. In Proceedings of the International Conference on Learning Representations, Virtual Event, 25–29 April 2022. Available online: https://openreview.n et/forum?id=yjMQuLLcGWK (accessed on 25 September 2025).
<!-- BLOCK_END: b_291 -->

<!-- BLOCK: b_292 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
34. Cao, X.; Yuan, P.; Feng, B.; Niu, K. CF-DETR: Coarse-to-Fine Transformers for End-to-End Object Detection. In Proceedings of the AAAI Conference on Artificial Intelligence, Online, 22 February–1 March 2022. Available online: https://api.semanticscholar.or g/CorpusID:250293790 (accessed on 25 September 2025).
<!-- BLOCK_END: b_292 -->

<!-- BLOCK: b_293 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
35. Li, F.; Zhang, H.; Liu, S.; Guo, J.; Ni, L.M.; Zhang, L. DN-DETR: Accelerate DETR Training by Introducing Query DeNoising. IEEE Trans. Pattern Anal. Mach. Intell. 2024, 46, 2239–2251. [CrossRef]
<!-- BLOCK_END: b_293 -->

<!-- BLOCK: b_294 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
36. Gao, Z.; Wang, L.; Han, B.; Guo, S. AdaMixer: A Fast-Converging Query-Based Object Detector. arXiv 2022, arXiv:2203.16507. [CrossRef]
<!-- BLOCK_END: b_294 -->

<!-- BLOCK: b_295 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
37. Chen, Z.; Zhang, J.; Tao, D. Recurrent Glimpse-based Decoder for Detection with Transformer. arXiv 2021, arXiv:2112.04632.
<!-- BLOCK_END: b_295 -->

<!-- BLOCK: b_296 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
38. Zhang, H.; Li, F.; Liu, S.; Zhang, L.; Su, H.; Zhu, J.; Ni, L.M.; Shum, H.Y. DINO: DETR with Improved DeNoising Anchor Boxes for End-to-End Object Detection. arXiv 2022, arXiv:2203.03605. [CrossRef]
<!-- BLOCK_END: b_296 -->

<!-- BLOCK: b_297 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
39. Zong, Z.; Song, G.; Liu, Y. DETRs with Collaborative Hybrid Assignments Training. In Proceedings of the 2023 IEEE/CVF International Conference on Computer Vision (ICCV), Paris, France, 2–6 October 2023; pp. 6725–6735. [CrossRef]
<!-- BLOCK_END: b_297 -->

<!-- BLOCK: b_298 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
40. Chen, Q.; Su, X.; Zhang, X.; Wang, J.; Chen, J.; Shen, Y.; Han, C.; Chen, Z.; Xu, W.; Li, F.; et al. LW-DETR: A Transformer Replacement to YOLO for Real-Time Detection. arXiv 2024, arXiv:2406.03459. Available online: https://arxiv.org/abs/2406.03459 (accessed on 25 September 2025).
<!-- BLOCK_END: b_298 -->

<!-- BLOCK: b_299 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
41. Zhao, Y.; Lv, W.; Xu, S.; Wei, J.; Wang, G.; Dang, Q.; Liu, Y.; Chen, J. DETRs Beat YOLOs on Real-time Object Detection. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), Seattle, WA, USA, 17–21 June 2024; pp. 16965–16974. Available online: https://openaccess.thecvf.com/content/CVPR2024/html/Zhao\_DETRs\_Beat\_YOLOs \_on\_Real-time\_Object\_Detection\_CVPR\_2024\_paper.html (accessed on 25 September 2025).
<!-- BLOCK_END: b_299 -->

<!-- BLOCK: b_300 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
42. Gu, J.; Wang, Z.; Kuen, J.; Ma, L.; Shahroudy, A.; Shuai, B.; Liu, T.; Wang, X.; Wang, G. Recent Advances in Convolutional Neural Networks. arXiv 2015, arXiv:1512.07108. [CrossRef]
<!-- BLOCK_END: b_300 -->

<!-- BLOCK: b_301 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
43. Borji, A.; Cheng, M.; Jiang, H.; Li, J. Salient Object Detection: A Survey. arXiv 2014, arXiv:1411.5878. [CrossRef]
<!-- BLOCK_END: b_301 -->

<!-- BLOCK: b_302 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
44. Chen, G.; Wang, H.; Chen, K.; Li, Z.; Song, Z.; Liu, Y.; Chen, W.; Knoll, A. A Survey of the Four Pillars for Small Object Detection: Multiscale Representation, Contextual Information, Super-Resolution, and Region Proposal. IEEE Trans. Syst. Man Cybern. Syst. 2022, 52, 936–953. [CrossRef]
<!-- BLOCK_END: b_302 -->

<!-- BLOCK: b_303 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
45. Agarwal, S.; du Terrail, J.O.; Jurie, F. Recent Advances in Object Detection in the Age of Deep Convolutional Neural Networks. arXiv 2018, arXiv:1809.03193.
<!-- BLOCK_END: b_303 -->

<!-- BLOCK: b_304 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
46. Yang, M.H.; Kriegman, D.; Ahuja, N. Detecting faces in images: A survey. IEEE Trans. Pattern Anal. Mach. Intell. 2002, 24, 34–58. [CrossRef]
<!-- BLOCK_END: b_304 -->

<!-- BLOCK: b_305 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
47. Zhao, B.; Feng, J.; Wu, X.; Yan, S. A survey on deep learning-based fine-grained object classification and semantic segmentation. Int. J. Autom. Comput. 2017, 14, 119–135. Available online: https://api.semanticscholar.org/CorpusID:53076119 (accessed on 25 September 2025). [CrossRef]
<!-- BLOCK_END: b_305 -->

<!-- BLOCK: b_306 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
48. Goswami, T.; Barad, Z.; Desai, P.; Nikita, P. Text Detection and Recognition in images: A survey. arXiv 2018, arXiv:1803.07278. [CrossRef]
<!-- BLOCK_END: b_306 -->

<!-- BLOCK: b_307 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
49. Chaudhari, S.; Polatkan, G.; Ramanath, R.; Mithal, V. An Attentive Survey of Attention Models. arXiv 2019, arXiv:1904.02874. [CrossRef]
<!-- BLOCK_END: b_307 -->

<!-- BLOCK: b_308 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
50. Han, J.; Zhang, D.; Cheng, G.; Liu, N.; Xu, D. Advanced Deep-Learning Techniques for Salient and Category-Specific Object Detection: A Survey. IEEE Signal Process. Mag. 2018, 35, 84–100. [CrossRef]
<!-- BLOCK_END: b_308 -->

<!-- BLOCK: b_309 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
51. Liu, L.; Ouyang, W.; Wang, X.; Fieguth, P.W.; Chen, J.; Liu, X.; Pietikäinen, M. Deep Learning for Generic Object Detection: A Survey. arXiv 2018, arXiv:1809.02165. [CrossRef]
<!-- BLOCK_END: b_309 -->

<!-- BLOCK: b_310 | type: bib_item | heading: Object Detection with Transformers: A Review > References -->
52. Enzweiler, M.; Gavrila, D.M. Monocular Pedestrian Detection: Survey and Experiments. IEEE Trans. Pattern Anal. Mach. Intell. 2009, 31, 2179–2195. [CrossRef]
<!-- BLOCK_END: b_310 -->

<!-- BLOCK: b_311 | type: list | heading: Object Detection with Transformers: A Review > References -->
53.
Ülkü, I.; Akagündüz, E. A Survey on Deep Learning-based Architectures for Semantic Segmentation on 2D images. arXiv 2019, arXiv:1912.10230.
54.
Cheng, G.; Han, J. A Survey on Object Detection in Optical Remote Sensing Images. arXiv 2016, arXiv:1603.06201. [CrossRef]
55.
Sommer, L.W.; Schuchert, T.; Beyerer, J. Fast Deep Vehicle Detection in Aerial Images.
In Proceedings of the 2017 IEEE Winter Conference on Applications of Computer Vision (WACV), Santa Rosa, CA, USA, 2–29 March 2017; pp. 311–319. [CrossRef]
56.
Zhang, P.; Niu, X.; Dou, Y.; Xia, F. Airport Detection on Optical Satellite Images Using Deep Convolutional Neural Networks.
IEEE Geosci.
Remote Sens.
Lett. 2017, 14, 1183–1187. [CrossRef]
57.
Bach, M.; Stumper, D.; Dietmayer, K. Deep Convolutional Traffic Light Recognition for Automated Driving.
In Proceedings of the 2018 21st International Conference on Intelligent Transportation Systems (ITSC), Maui, HI, USA, 4–7 November 2018; pp. 851–858. [CrossRef]
58. de la Escalera, A.; Moreno, L.; Salichs, M.; Armingol, J. Road traffic sign detection and classification.
IEEE Trans.
Ind.
Electron. 1997, 44, 848–859. [CrossRef]
59.
Shehzadi, T.; Hashmi, K.A.; Pagani, A.; Liwicki, M.; Stricker, D.; Afzal, M.Z. Mask-Aware Semi-Supervised Object Detection in Floor Plans.
Appl.
Sci. 2022, 12, 9398. [CrossRef]
60.
Hariharan, B.; Arbelaez, P.; Girshick, R.B.; Malik, J. Simultaneous Detection and Segmentation. arXiv 2014, arXiv:1407.1808. [CrossRef]
61.
Hariharan, B.; Arbeláez, P.A.; Girshick, R.B.; Malik, J. Hypercolumns for Object Segmentation and Fine-grained Localization. arXiv 2014, arXiv:1411.5752.
62.
Dai, J.; He, K.; Sun, J. Instance-aware Semantic Segmentation via Multi-task Network Cascades. arXiv 2015, arXiv:1512.04412.
63.
Karpathy, A.; Fei-Fei, L. Deep Visual-Semantic Alignments for Generating Image Descriptions. arXiv 2014, arXiv:1412.2306.
64.
Xu, K.; Ba, J.; Kiros, R.; Cho, K.; Courville, A.C.; Salakhutdinov, R.; Zemel, R.S.; Bengio, Y. Show, Attend and Tell: Neural Image Caption Generation with Visual Attention. arXiv 2015, arXiv:1502.03044.
65.
Wu, Q.; Shen, C.; van den Hengel, A.; Wang, P.; Dick, A.R. Image Captioning and Visual Question Answering Based on Attributes and Their Related External Knowledge. arXiv 2016, arXiv:1603.02814.
66.
Bai, S.; An, S. A survey on automatic image caption generation.
Neurocomputing 2018, 311, 291–304. [CrossRef]
67.
Kang, K.; Li, H.; Yan, J.; Zeng, X.; Yang, B.; Xiao, T.; Zhang, C.; Wang, Z.; Wang, R.; Wang, X.; et al. T-CNN: Tubelets with Convolutional Neural Networks for Object Detection from Videos. arXiv 2016, arXiv:1604.02532. [CrossRef]
68.
Arkin, E.; Yadikar, N.; Xu, X.; Aysa, A.; Ubul, K. A survey: Object detection methods from CNN to transformer.
Multimed.
Tools Appl. 2022, 82, 21353–21383. [CrossRef]
69.
Han, K.; Wang, Y.; Chen, H.; Chen, X.; Guo, J.; Liu, Z.; Tang, Y.; Xiao, A.; Xu, C.; Xu, Y.; et al. A Survey on Vision Transformer.
IEEE Trans.
Pattern Anal.
Mach.
Intell. 2023, 45, 87–110. [CrossRef]
70.
Arkin, E.; Yadikar, N.; Muhtar, Y.; Ubul, K. A Survey of Object Detection Based on CNN and Transformer.
In Proceedings of the 2021 IEEE 2nd International Conference on Pattern Recognition and Machine Learning (PRML), Chengdu, China, 16–18 July 2021; pp. 99–108. [CrossRef]
71.
Khan, S.; Naseer, M.; Hayat, M.; Zamir, S.W.; Khan, F.S.; Shah, M. Transformers in Vision: A Survey.
ACM Comput.
Surv. 2022, 54, 1–41. [CrossRef]
72.
Liu, S.; Li, F.; Zhang, H.; Yang, X.; Qi, X.; Su, H.; Zhu, J.; Zhang, L. DAB-DETR: Dynamic Anchor Boxes are Better Queries for DETR. arXiv 2022, arXiv:2201.12329. [CrossRef]
73.
Zou, Z.; Shi, Z.; Guo, Y.; Ye, J. Object Detection in 20 Years: A Survey. arXiv 2019, arXiv:1905.05055. [CrossRef]
74.
Zaidi, S.S.A.; Ansari, M.S.; Aslam, A.; Kanwal, N.; Asghar, M.N.; Lee, B. A Survey of Modern Deep Learning based Object Detection Models. arXiv 2021, arXiv:2104.11892. [CrossRef]
75.
Lin, T.; Maire, M.; Belongie, S.J.; Bourdev, L.D.; Girshick, R.B.; Hays, J.; Perona, P.; Ramanan, D.; Dollár, P.; Zitnick, C.L. Microsoft COCO: Common Objects in Context. arXiv 2014, arXiv:1405.0312.
76.
Jiao, L.; Zhang, F.; Liu, F.; Yang, S.; Li, L.; Feng, Z.; Qu, R. A Survey of Deep Learning-based Object Detection. arXiv 2019, arXiv:1907.09408. [CrossRef]
77.
Ahmed, M.; Hashmi, K.A.; Pagani, A.; Liwicki, M.; Stricker, D.; Afzal, M.Z. Survey and Performance Analysis of Deep Learning Based Object Detection in Challenging Environments.
Sensors 2021, 21, 5116. [CrossRef] [PubMed]
78.
Everingham, M.; Gool, L.V.; Williams, C.K.I.; Winn, J.; Zisserman, A. The Pascal Visual Object Classes (VOC) Challenge.
Int.
J. Comput.
Vis. 2009, 88, 303–308.
Available online: https://www.microsoft.com/en-us/research/publication/the-pascal-visual-o bject-classes-voc-challenge/ (accessed on 25 September 2025). [CrossRef]
79.
Lin, T.Y.; Dollár, P.; Girshick, R.; He, K.; Hariharan, B.; Belongie, S. Feature Pyramid Networks for Object Detection.
In Proceedings of the 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), Honolulu, HI, USA, 21–26 July 2017; pp. 936–944. [CrossRef]
80.
He, K.; Zhang, X.; Ren, S.; Sun, J. Deep Residual Learning for Image Recognition. arXiv 2015, arXiv:1512.03385. [CrossRef]
81.
Krizhevsky, A.; Sutskever, I.; Hinton, G.E. ImageNet Classification with Deep Convolutional Neural Networks.
In Proceedings of the Advances in Neural Information Processing Systems, Lake Tahoe, NV, USA, 3–6 December 2012; Pereira, F., Burges, C., Bottou, L., Weinberger, K., Eds.; Curran Associates, Inc.: Red Hook, NY, USA, 2012; Volume 25.
Available online: https: //proceedings.neurips.cc/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf (accessed on 25 September 2025).
82.
Bar, A.; Wang, X.; Kantorov, V.; Reed, C.J.; Herzig, R.; Chechik, G.; Rohrbach, A.; Darrell, T.; Globerson, A. DETReg: Unsupervised Pretraining with Region Priors for Object Detection. arXiv 2021, arXiv:2106.04550.
83.
Bateni, P.; Barber, J.; van de Meent, J.; Wood, F. Improving Few-Shot Visual Classification with Unlabelled Examples. arXiv 2020, arXiv:2006.12245.
84.
Wang, X.; Yang, X.; Zhang, S.; Li, Y.; Feng, L.; Fang, S.; Lyu, C.; Chen, K.; Zhang, W. Consistent Targets Provide Better Supervision in Semi-supervised Object Detection. arXiv 2022, arXiv:2209.01589. [CrossRef]
85.
Li, Y.; Huang, D.; Qin, D.; Wang, L.; Gong, B. Improving Object Detection with Selective Self-supervised Self-training. arXiv 2020, arXiv:2007.09162. [CrossRef]
86.
Hashmi, K.A.; Stricker, D.; Afzal, M.Z. Spatio-Temporal Learnable Proposals for End-to-End Video Object Detection. arXiv 2022, arXiv:2210.02368.
87.
Hashmi, K.A.; Pagani, A.; Stricker, D.; Afzal, M.Z. BoxMask: Revisiting Bounding Box Supervision for Video Object Detection.
In Proceedings of the 2023 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), Waikoloa, HI, USA, 2–7 January 2023; pp. 2029–2039. [CrossRef]
88.
Caron, M.; Touvron, H.; Misra, I.; Jégou, H.; Mairal, J.; Bojanowski, P.; Joulin, A. Emerging Properties in Self-Supervised Vision Transformers. arXiv 2021, arXiv:2104.14294. [CrossRef]
89.
Li, C.; Yang, J.; Zhang, P.; Gao, M.; Xiao, B.; Dai, X.; Yuan, L.; Gao, J. Efficient Self-supervised Vision Transformers for Representation Learning. arXiv 2021, arXiv:2106.09785.
90.
Liu, W.; Anguelov, D.; Erhan, D.; Szegedy, C.; Reed, S.E.; Fu, C.; Berg, A.C. SSD: Single Shot MultiBox Detector. arXiv 2015, arXiv:1512.02325.
91.
Redmon, J.; Divvala, S.K.; Girshick, R.B.; Farhadi, A. You Only Look Once: Unified, Real-Time Object Detection. arXiv 2015, arXiv:1506.02640.
92.
Redmon, J.; Farhadi, A. YOLO9000: Better, Faster, Stronger. arXiv 2016, arXiv:1612.08242. [CrossRef]
93.
Bochkovskiy, A.; Wang, C.; Liao, H.M. YOLOv4: Optimal Speed and Accuracy of Object Detection. arXiv 2020, arXiv:2004.10934. [CrossRef]
94.
Zhou, X.; Wang, D.; Krähenbühl, P. Objects as Points. arXiv 2019, arXiv:1904.07850.
95.
Fu, C.; Liu, W.; Ranga, A.; Tyagi, A.; Berg, A.C. DSSD: Deconvolutional Single Shot Detector. arXiv 2017, arXiv:1701.06659. [CrossRef]
96.
Jeong, J.; Park, H.; Kwak, N. Enhancement of SSD by concatenating feature maps for object detection. arXiv 2017, arXiv:1705.09587. [CrossRef]
97.
Zhang, S.; Wen, L.; Bian, X.; Lei, Z.; Li, S.Z. Single-Shot Refinement Neural Network for Object Detection. arXiv 2017, arXiv:1711.06897.
98.
Law, H.; Deng, J. CornerNet: Detecting Objects as Paired Keypoints. arXiv 2018, arXiv:1808.01244.
99.
He, K.; Zhang, X.; Ren, S.; Sun, J. Spatial Pyramid Pooling in Deep Convolutional Networks for Visual Recognition. arXiv 2014, arXiv:1406.4729.
100.
Dai, J.; Li, Y.; He, K.; Sun, J. R-FCN: Object Detection via Region-based Fully Convolutional Networks. arXiv 2016, arXiv:1605.06409.
101.
He, K.; Gkioxari, G.; Dollár, P.; Girshick, R. Mask R-CNN.
In Proceedings of the 2017 IEEE International Conference on Computer Vision (ICCV), Venice, Italy, 22–29 October 2017; pp. 2980–2988. [CrossRef]
102.
Qiao, S.; Chen, L.; Yuille, A.L. DetectoRS: Detecting Objects with Recursive Feature Pyramid and Switchable Atrous Convolution. arXiv 2020, arXiv:2006.02334. [CrossRef]
103.
Chen, K.; Pang, J.; Wang, J.; Xiong, Y.; Li, X.; Sun, S.; Feng, W.; Liu, Z.; Shi, J.; Ouyang, W.; et al. Hybrid Task Cascade for Instance Segmentation. arXiv 2019, arXiv:1901.07518. [CrossRef]
104.
Cai, Z.; Vasconcelos, N. Cascade R-CNN: Delving into High Quality Object Detection. arXiv 2017, arXiv:1712.00726. [CrossRef]
105.
Iandola, F.N.; Moskewicz, M.W.; Ashraf, K.; Han, S.; Dally, W.J.; Keutzer, K. SqueezeNet: AlexNet-level accuracy with 50x fewer parameters and <1MB model size. arXiv 2016, arXiv:1602.07360.
106.
Howard, A.G.; Zhu, M.; Chen, B.; Kalenichenko, D.; Wang, W.; Weyand, T.; Andreetto, M.; Adam, H. MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications. arXiv 2017, arXiv:1704.04861. [CrossRef]
107.
Sandler, M.; Howard, A.G.; Zhu, M.; Zhmoginov, A.; Chen, L. Inverted Residuals and Linear Bottlenecks: Mobile Networks for Classification, Detection and Segmentation. arXiv 2018, arXiv:1801.04381.
108.
Howard, A.; Sandler, M.; Chu, G.; Chen, L.; Chen, B.; Tan, M.; Wang, W.; Zhu, Y.; Pang, R.; Vasudevan, V.; et al. Searching for MobileNetV3. arXiv 2019, arXiv:1905.02244. [CrossRef]
109.
Zhang, X.; Zhou, X.; Lin, M.; Sun, J. ShuffleNet: An Extremely Efficient Convolutional Neural Network for Mobile Devices. arXiv 2017, arXiv:1707.01083. [CrossRef]
110.
Wang, R.J.; Li, X.; Ao, S.; Ling, C.X. Pelee: A Real-Time Object Detection System on Mobile Devices. arXiv 2018, arXiv:1804.06882.
111.
Ma, N.; Zhang, X.; Zheng, H.; Sun, J. ShuffleNet V2: Practical Guidelines for Efficient CNN Architecture Design. arXiv 2018, arXiv:1807.11164. [CrossRef]
112.
Tan, M.; Chen, B.; Pang, R.; Vasudevan, V.; Le, Q.V. MnasNet: Platform-Aware Neural Architecture Search for Mobile. arXiv 2018, arXiv:1807.11626.
113.
Yousaf, A.; Sazonov, E. Food Intake Detection in the Face of Limited Sensor Signal Annotations.
In Proceedings of the 2024 Tenth International Conference on Communications and Electronics (ICCE), Da Nang, Vietnam, 31 July–2 August 2024; pp. 351–356. [CrossRef]
114.
Cai, H.; Gan, C.; Han, S. Once for All: Train One Network and Specialize it for Efficient Deployment. arXiv 2019, arXiv:1908.09791.
115.
Chabot, F.; Chaouch, M.; Rabarisoa, J.; Teulière, C.; Chateau, T. Deep MANTA: A Coarse-to-fine Many-Task Network for joint 2D and 3D vehicle analysis from monocular image. arXiv 2017, arXiv:1703.07570.
116.
Mousavian, A.; Anguelov, D.; Flynn, J.; Kosecka, J. 3D Bounding Box Estimation Using Deep Learning and Geometry. arXiv 2016, arXiv:1612.00496.
117.
Li, B.; Ouyang, W.; Sheng, L.; Zeng, X.; Wang, X. GS3D: An Efficient 3D Object Detection Framework for Autonomous Driving. arXiv 2019, arXiv:1903.10955. [CrossRef]
118.
Li, P.; Chen, X.; Shen, S. Stereo R-CNN based 3D Object Detection for Autonomous Driving. arXiv 2019, arXiv:1902.09738. [CrossRef]
119.
Shi, X.; Ye, Q.; Chen, X.; Chen, C.; Chen, Z.; Kim, T. Geometry-based Distance Decomposition for Monocular 3D Object Detection. arXiv 2021, arXiv:2104.03775.
120.
Ma, X.; Zhang, Y.; Xu, D.; Zhou, D.; Yi, S.; Li, H.; Ouyang, W. Delving into Localization Errors for Monocular 3D Object Detection. arXiv 2021, arXiv:2103.16237. [CrossRef]
121.
Liu, Y.; Wang, L.; Liu, M. YOLOStereo3D: A Step Back to 2D for Efficient Stereo 3D Detection. arXiv 2021, arXiv:2103.09422. [CrossRef]
122.
Yin, T.; Zhou, X.; Krähenbühl, P. Center-based 3D Object Detection and Tracking. arXiv 2020, arXiv:2006.11275.
123.
Zhou, Y.; Tuzel, O. VoxelNet: End-to-End Learning for Point Cloud Based 3D Object Detection. arXiv 2017, arXiv:1711.06396.
124.
Lang, A.H.; Vora, S.; Caesar, H.; Zhou, L.; Yang, J.; Beijbom, O. PointPillars: Fast Encoders for Object Detection from Point Clouds. arXiv 2018, arXiv:1812.05784.
125.
Xu, Q.; Zhong, Y.; Neumann, U. Behind the Curtain: Learning Occluded Shapes for 3D Object Detection. arXiv 2021, arXiv:2112.02205. [CrossRef]
126.
Zheng, W.; Tang, W.; Chen, S.; Jiang, L.; Fu, C. CIA-SSD: Confident IoU-Aware Single-Stage Object Detector from Point Cloud. arXiv 2020, arXiv:2012.03015. [CrossRef]
127.
Zheng, W.; Tang, W.; Jiang, L.; Fu, C. SE-SSD: Self-Ensembling Single-Stage Object Detector From Point Cloud. arXiv 2021, arXiv:2104.09804.
128.
Deng, J.; Shi, S.; Li, P.; Zhou, W.; Zhang, Y.; Li, H. Voxel R-CNN: Towards High Performance Voxel-based 3D Object Detection. arXiv 2020, arXiv:2012.15712. [CrossRef]
129.
Sheng, H.; Cai, S.; Liu, Y.; Deng, B.; Huang, J.; Hua, X.; Zhao, M. Improving 3D Object Detection with Channel-wise Transformer. arXiv 2021, arXiv:2108.10723. [CrossRef]
130.
Mao, J.; Xue, Y.; Niu, M.; Bai, H.; Feng, J.; Liang, X.; Xu, H.; Xu, C. Voxel Transformer for 3D Object Detection. arXiv 2021, arXiv:2109.02497. [CrossRef]
131.
Vora, S.; Lang, A.H.; Helou, B.; Beijbom, O. PointPainting: Sequential Fusion for 3D Object Detection. arXiv 2019, arXiv:1911.10150.
132.
Ku, J.; Mozifian, M.; Lee, J.; Harakeh, A.; Waslander, S.L. Joint 3D Proposal Generation and Object Detection from View Aggregation. arXiv 2017, arXiv:1712.02294.
133.
Liang, M.; Yang, B.; Wang, S.; Urtasun, R. Deep Continuous Fusion for Multi-Sensor 3D Object Detection. arXiv 2020, arXiv:2012.10992. [CrossRef]
134.
Yoo, J.H.; Kim, Y.; Kim, J.S.; Choi, J.W. 3D-CVF: Generating Joint Camera and LiDAR Features Using Cross-View Spatial Feature Fusion for 3D Object Detection. arXiv 2020, arXiv:2004.12636.
135.
Pang, S.; Morris, D.; Radha, H. CLOCs: Camera-LiDAR Object Candidates Fusion for 3D Object Detection. arXiv 2020, arXiv:2009.00784.
136.
Ye, L.; Rochan, M.; Liu, Z.; Wang, Y. Cross-Modal Self-Attention Network for Referring Image Segmentation. arXiv 2019, arXiv:1904.04745.
137.
Xie, E.; Wang, W.; Yu, Z.; Anandkumar, A.; Alvarez, J.M.; Luo, P. SegFormer: Simple and Efficient Design for Semantic Segmentation with Transformers. arXiv 2021, arXiv:2105.15203. [CrossRef]
138.
Zheng, S.; Lu, J.; Zhao, H.; Zhu, X.; Luo, Z.; Wang, Y.; Fu, Y.; Feng, J.; Xiang, T.; Torr, P.H.S.; et al. Rethinking Semantic Segmentation from a Sequence-to-Sequence Perspective with Transformers. arXiv 2020, arXiv:2012.15840.
139.
Strudel, R.; Pinel, R.G.; Laptev, I.; Schmid, C. Segmenter: Transformer for Semantic Segmentation. arXiv 2021, arXiv:2105.05633. [CrossRef]
140.
Ramachandran, P.; Parmar, N.; Vaswani, A.; Bello, I.; Levskaya, A.; Shlens, J. Stand-Alone Self-Attention in Vision Models. arXiv 2019, arXiv:1906.05909.
141.
Wang, W.; Xie, E.; Li, X.; Fan, D.; Song, K.; Liang, D.; Lu, T.; Luo, P.; Shao, L. Pyramid Vision Transformer: A Versatile Backbone for Dense Prediction without Convolutions. arXiv 2021, arXiv:2102.12122. [CrossRef]
142.
Kirillov, A.; He, K.; Girshick, R.B.; Rother, C.; Dollár, P. Panoptic Segmentation. arXiv 2018, arXiv:1801.00868.
143.
Wang, H.; Zhu, Y.; Green, B.; Adam, H.; Yuille, A.L.; Chen, L. Axial-DeepLab: Stand-Alone Axial-Attention for Panoptic Segmentation. arXiv 2020, arXiv:2003.07853.
144.
Neuhold, G.; Ollmann, T.; Bulò, S.R.; Kontschieder, P. The Mapillary Vistas Dataset for Semantic Understanding of Street Scenes.
In Proceedings of the 2017 IEEE International Conference on Computer Vision (ICCV), Venice, Italy, 22–29 October 2017; pp. 5000–5009. [CrossRef]
145.
Cordts, M.; Omran, M.; Ramos, S.; Rehfeld, T.; Enzweiler, M.; Benenson, R.; Franke, U.; Roth, S.; Schiele, B. The Cityscapes Dataset for Semantic Urban Scene Understanding. arXiv 2016, arXiv:1604.01685. [CrossRef]
146.
Reed, S.; Akata, Z.; Yan, X.; Logeswaran, L.; Schiele, B.; Lee, H. Generative Adversarial Text to Image Synthesis.
In Proceedings of the 33rd International Conference on Machine Learning, New York, NY, USA, 20–22 June 2016; Balcan, M.F., Weinberger, K.Q., Eds.; Proceedings of Machine Learning Research: New York, NY, USA, 2016; Volume 48, pp. 1060–1069.
Available online: https://proceedings.mlr.press/v48/reed16.html (accessed on 25 September 2025).
147.
Zhang, H.; Xu, T.; Li, H.; Zhang, S.; Huang, X.; Wang, X.; Metaxas, D.N. StackGAN: Text to Photo-realistic Image Synthesis with Stacked Generative Adversarial Networks. arXiv 2016, arXiv:1612.03242.
148.
Zhang, H.; Xu, T.; Li, H.; Zhang, S.; Wang, X.; Huang, X.; Metaxas, D.N. StackGAN++: Realistic Image Synthesis with Stacked Generative Adversarial Networks. arXiv 2017, arXiv:1710.10916.
149.
Xu, T.; Zhang, P.; Huang, Q.; Zhang, H.; Gan, Z.; Huang, X.; He, X. AttnGAN: Fine-Grained Text to Image Generation with Attentional Generative Adversarial Networks. arXiv 2017, arXiv:1711.10485.
150.
Goodfellow, I.J.; Pouget-Abadie, J.; Mirza, M.; Xu, B.; Warde-Farley, D.; Ozair, S.; Courville, A.; Bengio, Y. Generative Adversarial Networks. arXiv 2014, arXiv:1406.2661. [CrossRef]
151.
Murahari, M.D.; Reddy; Sk, M.; Basha, M.M.M.; Hari, M.N.C.; Student, P. DALL-E: CREATING IMAGES FROM TEXT. 2021.
Available online: https://api.semanticscholar.org/CorpusID:261026641 (accessed on 25 September 2025).
152.
Wang, X.; Yeshwanth, C.; Nießner, M. SceneFormer: Indoor Scene Generation with Transformers. arXiv 2020, arXiv:2012.09793.
153.
Chen, M.; Radford, A.; Child, R.; Wu, J.; Jun, H.; Luan, D.; Sutskever, I. Generative Pretraining From Pixels.
In Proceedings of the 37th International Conference on Machine Learning, Virtual Event, 13–18 July 2020; III, H.D., Singh, A., Eds.; Proceedings of Machine Learning Research (PMLR): New York, NY, USA, 2020; Volume 119, pp. 1691–1703.
Available online: https: //proceedings.mlr.press/v119/chen20s.html (accessed on 25 September 2025).
154.
Esser, P.; Rombach, R.; Ommer, B. Taming Transformers for High-Resolution Image Synthesis. arXiv 2020, arXiv:2012.09841.
155.
Jiang, Y.; Chang, S.; Wang, Z. TransGAN: Two Transformers Can Make One Strong GAN. arXiv 2021, arXiv:2102.07074.
156.
Bhunia, A.K.; Khan, S.H.; Cholakkal, H.; Anwer, R.M.; Khan, F.S.; Shah, M. Handwriting Transformers. arXiv 2021, arXiv:2104.03964. [CrossRef]
157.
Krizhevsky, A.; Hinton, G. Learning Multiple Layers of Features from Tiny Images; Technical Report; University of Toronto: Toronto, ON, Canada, 2009.
Available online: https://www.cs.toronto.edu/\~kriz/learning-features-2009-TR.pdf (accessed on 25 September 2025).
158.
Coates, A.; Ng, A.; Lee, H. An Analysis of Single-Layer Networks in Unsupervised Feature Learning.
In Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics, Fort Lauderdale, FL, USA, 11–13 April 2011; Gordon, G., Dunson, D., Dudík, M., Eds.; Proceedings of Machine Learning Research: New York, NY, USA, 2011; Volume 15, pp. 215–223.
Available online: https://proceedings.mlr.press/v15/coates11a.html (accessed on 25 September 2025).
159.
Chen, T.; Kornblith, S.; Norouzi, M.; Hinton, G.E. A Simple Framework for Contrastive Learning of Visual Representations. arXiv 2020, arXiv:2002.05709. [CrossRef]
160.
Deng, J.; Dong, W.; Socher, R.; Li, L.J.; Li, K.; Fei-Fei, L. ImageNet: A large-scale hierarchical image database.
In Proceedings of the 2009 IEEE Conference on Computer Vision and Pattern Recognition, Miami, FL, USA, 20–25 June 2009; pp. 248–255. [CrossRef]
161.
He, K.; Fan, H.; Wu, Y.; Xie, S.; Girshick, R.B. Momentum Contrast for Unsupervised Visual Representation Learning. arXiv 2019, arXiv:1911.05722.
162.
Bachman, P.; Hjelm, R.D.; Buchwalter, W. Learning Representations by Maximizing Mutual Information Across Views. arXiv 2019, arXiv:1906.00910. [CrossRef]
163.
Hénaff, O.J.; Srinivas, A.; Fauw, J.D.; Razavi, A.; Doersch, C.; Eslami, S.M.A.; van den Oord, A. Data-Efficient Image Recognition with Contrastive Predictive Coding. arXiv 2019, arXiv:1905.09272.
164.
Radford, A.; Metz, L.; Chintala, S. Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks. arXiv 2015, arXiv:1511.06434.
Available online: https://api.semanticscholar.org/CorpusID:11758569 (accessed on 25 September 2025).
165.
Gao, C.; Chen, Y.; Liu, S.; Tan, Z.; Yan, S. AdversarialNAS: Adversarial Neural Architecture Search for GANs. arXiv 2019, arXiv:1912.02037.
166.
Karras, T.; Laine, S.; Aittala, M.; Hellsten, J.; Lehtinen, J.; Aila, T. Analyzing and Improving the Image Quality of StyleGAN. arXiv 2019, arXiv:1912.04958.
167.
Yang, F.; Yang, H.; Fu, J.; Lu, H.; Guo, B. Learning Texture Transformer Network for Image Super-Resolution. arXiv 2020, arXiv:2006.04139. [CrossRef]
168.
Chen, H.; Wang, Y.; Guo, T.; Xu, C.; Deng, Y.; Liu, Z.; Ma, S.; Xu, C.; Xu, C.; Gao, W. Pre-Trained Image Processing Transformer. arXiv 2020, arXiv:2012.00364.
169.
Liang, J.; Cao, J.; Sun, G.; Zhang, K.; Van Gool, L.; Timofte, R. SwinIR: Image Restoration Using Swin Transformer. arXiv 2021, arXiv:2108.10257. [CrossRef]
170.
Wang, Z.; Cun, X.; Bao, J.; Liu, J. Uformer: A General U-Shaped Transformer for Image Restoration. arXiv 2021, arXiv:2106.03106. [CrossRef]
171.
Kumar, M.; Weissenborn, D.; Kalchbrenner, N. Colorization Transformer. arXiv 2021, arXiv:2102.04432.
172.
Antol, S.; Agrawal, A.; Lu, J.; Mitchell, M.; Batra, D.; Zitnick, C.L.; Parikh, D. VQA: Visual Question Answering. arXiv 2015, arXiv:1505.00468.
173.
Zellers, R.; Bisk, Y.; Farhadi, A.; Choi, Y. From Recognition to Cognition: Visual Commonsense Reasoning. arXiv 2018, arXiv:1811.10830.
174.
Lee, K.; Chen, X.; Hua, G.; Hu, H.; He, X. Stacked Cross Attention for Image-Text Matching. arXiv 2018, arXiv:1803.08024. [CrossRef]
175.
Vinyals, O.; Toshev, A.; Bengio, S.; Erhan, D. Show and Tell: A Neural Image Caption Generator. arXiv 2014, arXiv:1411.4555.
176.
Chen, Y.; Li, L.; Yu, L.; Kholy, A.E.; Ahmed, F.; Gan, Z.; Cheng, Y.; Liu, J. UNITER: Learning UNiversal Image-TExt Representations. arXiv 2019, arXiv:1909.11740.
177.
Li, X.; Yin, X.; Li, C.; Zhang, P.; Hu, X.; Zhang, L.; Wang, L.; Hu, H.; Dong, L.; Wei, F.; et al. Oscar: Object-Semantics Aligned Pre-training for Vision-Language Tasks. arXiv 2020, arXiv:2004.06165.
178.
Sun, C.; Myers, A.; Vondrick, C.; Murphy, K.; Schmid, C. VideoBERT: A Joint Model for Video and Language Representation Learning. arXiv 2019, arXiv:1904.01766. [CrossRef]
179.
Li, G.; Duan, N.; Fang, Y.; Jiang, D.; Zhou, M. Unicoder-VL: A Universal Encoder for Vision and Language by Cross-modal Pre-training. arXiv 2019, arXiv:1908.06066. [CrossRef]
180.
Li, L.H.; Yatskar, M.; Yin, D.; Hsieh, C.; Chang, K. VisualBERT: A Simple and Performant Baseline for Vision and Language. arXiv 2019, arXiv:1908.03557. [CrossRef]
181.
Su, W.; Zhu, X.; Cao, Y.; Li, B.; Lu, L.; Wei, F.; Dai, J. VL-BERT: Pre-training of Generic Visual-Linguistic Representations. arXiv 2019, arXiv:1908.08530.
182.
Tan, H.; Bansal, M. LXMERT: Learning Cross-Modality Encoder Representations from Transformers. arXiv 2019, arXiv:1908.07490. [CrossRef]
183.
Lu, J.; Batra, D.; Parikh, D.; Lee, S. ViLBERT: Pretraining Task-Agnostic Visiolinguistic Representations for Vision-and-Language Tasks. arXiv 2019, arXiv:1908.02265.
184.
Lee, S.; Yu, Y.; Kim, G.; Breuel, T.M.; Kautz, J.; Song, Y. Parameter Efficient Multimodal Transformers for Video Representation Learning. arXiv 2020, arXiv:2012.04124.
185.
Sun, N.; Zhu, Y.; Hu, X. Faster R-CNN Based Table Detection Combining Corner Locating.
In Proceedings of the 2019 International Conference on Document Analysis and Recognition (ICDAR), Sydney, NSW, Australia, 20–25 September 2019; pp. 1314–1319. [CrossRef]
186.
Parmar, N.; Vaswani, A.; Uszkoreit, J.; Kaiser, L.; Shazeer, N.; Ku, A. Image Transformer. arXiv 2018, arXiv:1802.05751.
187.
Bello, I.; Zoph, B.; Vaswani, A.; Shlens, J.; Le, Q.V. Attention Augmented Convolutional Networks. arXiv 2019, arXiv:1904.09925.
188.
Rezatofighi, S.H.; Tsoi, N.; Gwak, J.; Sadeghian, A.; Reid, I.D.; Savarese, S. Generalized Intersection over Union: A Metric and a Loss for Bounding Box Regression. arXiv 2019, arXiv:1902.09630. [CrossRef]
189. van den Oord, A.; Li, Y.; Babuschkin, I.; Simonyan, K.; Vinyals, O.; Kavukcuoglu, K.; van den Driessche, G.; Lockhart, E.; Cobo, L.C.; Stimberg, F.; et al. Parallel WaveNet: Fast High-Fidelity Speech Synthesis. arXiv 2017, arXiv:1711.10433.
190.
Gu, J.; Bradbury, J.; Xiong, C.; Li, V.O.K.; Socher, R. Non-Autoregressive Neural Machine Translation. arXiv 2017, arXiv:1711.02281.
191.
Ghazvininejad, M.; Levy, O.; Liu, Y.; Zettlemoyer, L. Mask-Predict: Parallel Decoding of Conditional Masked Language Models.
In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), Hong Kong, China, 3–7 November 2019; Inui, K., Jiang, J., Ng, V., Wan, X., Eds.; Association for Computational Linguistics: Stroudsburg, PA, USA, 2019; pp. 6112–6121. [CrossRef]
192.
Stewart, R.; Andriluka, M. End-to-end people detection in crowded scenes. arXiv 2015, arXiv:1506.04878.
193.
Romera-Paredes, B.; Torr, P.H.S. Recurrent Instance Segmentation. arXiv 2015, arXiv:1511.08250.
194.
Park, E.; Berg, A.C. Learning to decompose for object detection and instance segmentation. arXiv 2015, arXiv:1511.06449.
195.
Ren, M.; Zemel, R.S. End-to-End Instance Segmentation and Counting with Recurrent Attention. arXiv 2016, arXiv:1605.09410.
196.
Salvador, A.; Bellver, M.; Baradad, M.; Marqués, F.; Torres, J.; Giró-i-Nieto, X. Recurrent Neural Networks for Semantic Instance Segmentation. arXiv 2017, arXiv:1712.00617.
197.
Dai, J.; Qi, H.; Xiong, Y.; Li, Y.; Zhang, G.; Hu, H.; Wei, Y. Deformable Convolutional Networks. arXiv 2017, arXiv:1703.06211. [CrossRef]
198.
Zhu, X.; Hu, H.; Lin, S.; Dai, J. Deformable ConvNets v2: More Deformable, Better Results. arXiv 2018, arXiv:1811.11168. [CrossRef]
199.
Zhang, H.; Wang, J. Towards Adversarially Robust Object Detection. arXiv 2019, arXiv:1907.10310. [CrossRef]
200.
Wu, Y.; Chen, Y.; Yuan, L.; Liu, Z.; Wang, L.; Li, H.; Fu, Y. Rethinking Classification and Localization in R-CNN. arXiv 2019, arXiv:1904.06493. [CrossRef]
201.
Song, G.; Liu, Y.; Wang, X. Revisiting the Sibling Head in Object Detector. arXiv 2020, arXiv:2003.07540. [CrossRef]
202.
Dong, L.; Yang, N.; Wang, W.; Wei, F.; Liu, X.; Wang, Y.; Gao, J.; Zhou, M.; Hon, H. Unified Language Model Pre-training for Natural Language Understanding and Generation. arXiv 2019, arXiv:1905.03197. [CrossRef]
203.
Srivastava, N.; Hinton, G.; Krizhevsky, A.; Sutskever, I.; Salakhutdinov, R. Dropout: A Simple Way to Prevent Neural Networks from Overfitting.
J. Mach.
Learn.
Res. 2014, 15, 1929–1958.
Available online: http://jmlr.org/papers/v15/srivastava14a.html (accessed on 25 September 2025).
204.
Sun, P.; Zhang, R.; Jiang, Y.; Kong, T.; Xu, C.; Zhan, W.; Tomizuka, M.; Li, L.; Yuan, Z.; Wang, C.; et al. Sparse R-CNN: End-to-End Object Detection with Learnable Proposals. arXiv 2020, arXiv:2011.12450.
205.
Zhang, X.; Wan, F.; Liu, C.; Ji, R.; Ye, Q. FreeAnchor: Learning to Match Anchors for Visual Object Detection. arXiv 2019, arXiv:1909.02466. [CrossRef]
206.
Kim, K.; Lee, H.S. Probabilistic Anchor Assignment with IoU Prediction for Object Detection. arXiv 2020, arXiv:2007.08103. [CrossRef]
207.
Li, H.; Wu, Z.; Zhu, C.; Xiong, C.; Socher, R.; Davis, L.S. Learning from Noisy Anchors for One-stage Object Detection. arXiv 2019, arXiv:1912.05086.
208.
Tian, Z.; Shen, C.; Chen, H.; He, T. FCOS: Fully Convolutional One-Stage Object Detection.
In Proceedings of the 2019 IEEE/CVF International Conference on Computer Vision (ICCV), Seoul, Republic of Korea, 27 October–2 November 2019; pp. 9626–9635. [CrossRef]
209.
Wu, Y.; He, K. Group Normalization. arXiv 2018, arXiv:1803.08494. [CrossRef]
210.
Chen, Y.; Kalantidis, Y.; Li, J.; Yan, S.; Feng, J. A2-Nets: Double Attention Networks. arXiv 2018, arXiv:1810.11579.
211.
Lin, T.Y.; RoyChowdhury, A.; Maji, S. Bilinear CNN Models for Fine-Grained Visual Recognition.
In Proceedings of the 2015 IEEE International Conference on Computer Vision (ICCV), Santiago, Chile, 7–13 December 2015; pp. 1449–1457. [CrossRef]
212.
Wang, X.; Zhang, S.; Yu, Z.; Feng, L.; Zhang, W. Scale-Equalizing Pyramid Convolution for Object Detection.
In Proceedings of the 2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), Seattle, WA, USA, 13–19 June 2020; pp. 13356–13365.
Available online: https://api.semanticscholar.org/CorpusID:218537867 (accessed on 25 September 2025).
213.
Hu, J.; Shen, L.; Sun, G. Squeeze-and-Excitation Networks. arXiv 2017, arXiv:1709.01507.
214.
Jiang, Z.; Yu, W.; Zhou, D.; Chen, Y.; Feng, J.; Yan, S. ConvBERT: Improving BERT with Span-based Dynamic Convolution. arXiv 2020, arXiv:2008.02496.
215.
Beal, J.; Kim, E.; Tzeng, E.; Park, D.H.; Zhai, A.; Kislyuk, D. Toward Transformer-Based Object Detection. arXiv 2020, arXiv:2012.09958. [CrossRef]
216.
Zhu, B.; Wang, J.; Jiang, Z.; Zong, F.; Liu, S.; Li, Z.; Sun, J. AutoAssign: Differentiable Label Assignment for Dense Object Detection. arXiv 2020, arXiv:2007.03496. [CrossRef]
217.
Hendrycks, D.; Gimpel, K. Bridging Nonlinearities and Stochastic Regularizers with Gaussian Error Linear Units. arXiv 2016, arXiv:1606.08415. [CrossRef]
218.
Ba, J.L.; Kiros, J.R.; Hinton, G.E. Layer Normalization. arXiv 2016, arXiv:1607.06450. [CrossRef]
219.
Ma, X.; Kong, X.; Wang, S.; Zhou, C.; May, J.; Ma, H.; Zettlemoyer, L. Luna: Linear Unified Nested Attention. arXiv 2021, arXiv:2106.01540. [CrossRef]
220.
Shen, Z.; Zhang, M.; Yi, S.; Yan, J.; Zhao, H. Factorized Attention: Self-Attention with Linear Complexities. arXiv 2018, arXiv:1812.01243.
221.
Ge, Z.; Liu, S.; Wang, F.; Li, Z.; Sun, J. YOLOX: Exceeding YOLO Series in 2021. arXiv 2021, arXiv:2107.08430. [CrossRef]
222.
Oquab, M.; Darcet, T.; Moutakanni, T.; Vo, H.; Szafraniec, M.; Khalidov, V.; Fernandez, P.; Haziza, D.; Massa, F.; El-Nouby, A.; et al. DINOv2: Learning Robust Visual Features without Supervision. arXiv 2024, arXiv:2304.07193.
Available online: https://arxiv.org/abs/2304.07193 (accessed on 25 September 2025). [CrossRef]
223.
Siméoni, O.; Vo, H.V.; Seitzer, M.; Baldassarre, F.; Oquab, M.; Jose, C.; Khalidov, V.; Szafraniec, M.; Yi, S.; Ramamonjisoa, M.; et al. DINOv3. arXiv 2025, arXiv:2508.10104.
Available online: https://arxiv.org/abs/2508.10104 (accessed on 25 September 2025). [PubMed]
224.
Lv, W.; Zhao, Y.; Chang, Q.; Huang, K.; Wang, G.; Liu, Y. RT-DETRv2: Improved Baseline with Bag-of-Freebies for Real-Time Detection Transformer. arXiv 2024, arXiv:2407.17140.
Available online: https://arxiv.org/abs/2407.17140 (accessed on 25 September 2025).
225.
Wang, S.; Xia, C.; Lv, F.; Shi, Y. RT-DETRv3: Real-time End-to-End Object Detection with Hierarchical Dense Positive Supervision. arXiv 2024, arXiv:2409.08475.
226.
Powers, D.M.W. Evaluation: From precision, recall and F-measure to ROC, informedness, markedness and correlation. arXiv 2020, arXiv:2010.16061. [CrossRef]
227.
Touvron, H.; Cord, M.; Douze, M.; Massa, F.; Sablayrolles, A.; Jégou, H. Training data-efficient image transformers & distillation through attention. arXiv 2020, arXiv:2012.12877.
228.
Liu, Z.; Lin, Y.; Cao, Y.; Hu, H.; Wei, Y.; Zhang, Z.; Lin, S.; Guo, B. Swin Transformer: Hierarchical Vision Transformer using Shifted Windows. arXiv 2021, arXiv:2103.14030. [CrossRef]
<!-- BLOCK_END: b_311 -->

<!-- BLOCK: b_312 | type: paragraph | heading: Object Detection with Transformers: A Review > References -->
免责声明/出版者注：所有出版物中包含的声明、观点和数据仅为个人作者和贡献者所有，而非 MDPI 和/或编辑者所有。
MDPI 和/或编辑者对因内容中提及的任何想法、方法、指示或产品而导致的对人身或财产的任何伤害不承担责任。
<!-- BLOCK_END: b_312 -->
