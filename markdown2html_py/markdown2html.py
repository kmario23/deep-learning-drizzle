from pyemojify import emojify
import re
import markdown
from lxml import etree


# read contents from github README.md
with open('README.md', 'r') as f:
    markdn = f.readlines()

# read some header contents for html
with open('html_head.txt', 'r') as f:
    html_head = f.readlines()

# read some footer contents for html
with open('html_foot.txt', 'r') as f:
    html_foot = f.readlines()

# read some fontawesome stuff for html
with open('fontawesome-animations.txt', 'r') as f:
    fontawesome_animations = []
    for line in f:
        line = line.strip().replace('BEG:', '')
        line = line.strip().replace('END:', '')
        fontawesome_animations.append(line)

# to color code the emojies
em1 = '<i class="em em-'
em2 = '"></i>'

# link to specific part of page
ahref1 = '<a href="'
ahrefm = '" style="text-decoration:none">'
ahref2 = '</a>'

host_url = "https://deep-learning-drizzle.github.io/"
host_page = "index.html"

# heading size 1
h1b = "<h1> "
h1e = " </h1>"

# heading size 2
h2b = "<h2>"
h2e = " </h2>"

# heading size 5
h5b = "<h5>"
h5e = "</h5>"

# line break html
lb_html = '<br/>'

# html url construction
url1 = '<a href="'
url2 = ' "style="text-decoration:none">'
url3 = '</a>'

# center align something
center1 = '<p style="text-align:center">'
center2 = '</p>'

# navigation to toc
g2c = "Go to Contents "
divcont = '#contents'

# navigation to top of table
divdnns = '#dldnn'
divmlfund = '#mlfund'
divopt4ml = '#opt4ml'
divgenml = '#genml'
divreinf = '#reinf'
divbdl = '#bayesdl'
divmi = '#medimg'
divpgm = '#probgm'
divgnn = '#graphnn'
divnlp = '#nlpnn'
divasr = '#asrnn'
divcvnn = '#cvnn'
divbcss = '#bcss'
divagi = '#aginn'


def prettify_emoji(word):
    return em1 + word + em2


# down arrow
down_arrow = ":arrow_heading_down:"
down_arrow_prettified = prettify_emoji("arrow_heading_down")

# up arrow
up_arrow = ":arrow_heading_up:"
up_arrow_prettified = prettify_emoji("arrow_heading_up")


def parse_markdown_url(text):
    """
    A simple helper function to convert markdwon url to a tuple:
    [url_text](https://) => ('url_text', 'https://')
    From: https://stackoverflow.com/a/23395483
    """
    # Anything that isn't a square closing bracket
    name_regex = "[^]]+"
    # http:// or https:// followed by anything but a closing paren
    url_regex = "http[s]?://[^)]+"

    markup_regex = '\[({0})]\(\s*({1})\s*\)'.format(name_regex, url_regex)

    extracted = []
    for match in re.findall(markup_regex, text):
        extracted.append(match)
    return extracted

# s = '| 1.   | **Neural Networks for Machine Learning**              | Geoffrey Hinton, University of Toronto         | [Lecture-Slides](http://www.cs.toronto.edu/~hinton/coursera_slides.html) <br/> [CSC321-tijmen](https://www.cs.toronto.edu/~tijmen/csc321/) | [YouTube-Lectures](https://www.youtube.com/playlist?list=PLoRl3Ht4JOcdU872GhiYWf6jwrk_SNhz9) <br/> [UofT-mirror](https://www.cs.toronto.edu/~hinton/coursera_lectures.html) | 2012 <br/> 2014 |'
# print(parse_markdown_url(s))


def convert_markdown_url2html(text, extracted):
    if len(extracted) == 1:
        url_text, url_link = extracted[0][0], extracted[0][1]
        text = text.replace(url_text, "")
        text = text.replace(url_link, "")
        url = url1 + url_link + url2 + url_text + url3
        text = text.replace("[]()", url)

        # center align
        text = center1 + text + center2
        return text


def table_topic_emoji_processor(line):
    if ":" in line:
        matches = re.findall(r":(.*?):", line)
        # print(matches)
        for emj in matches:
            m = ":" + emj + ":"
            if m in line:
                # line = line.replace(m, prettify_emoji(emj)) # uncomment this line to enable emojis
                line = line.replace(m, '')
    return line.strip()


def add_navigation_button():
    """
    adds a go to contents button
    """
    pret = prettify_emoji("arrow_heading_up")
    pret = url1 + host_url + host_page + divcont + url2 + h5b + g2c + pret + h5e + url3
    return pret


def replace_github_url_with_webpage_url(line, matches):
    for lnk in matches:
        lnk = lnk.replace('(', '')
        lnk = lnk.replace(')', '')
        if "deep-learning-deep-neural-networks" in line:
            line = line.replace(lnk, host_url + host_page + divdnns)
        if "probabilistic-graphical-models" in line:
            line = line.replace(lnk, host_url + host_page + divpgm)
        if "bayesian-deep-learning" in line:
            line = line.replace(lnk, host_url + host_page + divbdl)
        if "medical-imaging" in line:
            line = line.replace(lnk, host_url + host_page + divmi)
        if "machine-learning-fundamentals" in line:
            line = line.replace(lnk, host_url + host_page + divmlfund)
        if "natural-language-processing" in line:
            line = line.replace(lnk, host_url + host_page + divnlp)
        if "optimization-for-machine-learning" in line:
            line = line.replace(lnk, host_url + host_page + divopt4ml)
        if "automatic-speech-recognition-speech" in line:
            line = line.replace(lnk, host_url + host_page + divasr)
        if "general-machine-learning" in line:
            line = line.replace(lnk, host_url + host_page + divgenml)
        if "modern-computer-vision" in line:
            line = line.replace(lnk, host_url + host_page + divcvnn)
        if "reinforcement-learning" in line:
            line = line.replace(lnk, host_url + host_page + divreinf)
        if "boot-camps-or-summer-schools" in line:
            line = line.replace(lnk, host_url + host_page + divbcss)
        if "graph-neural-networks" in line:
            line = line.replace(lnk, host_url + host_page + divgnn)
        if "birds-eye-view-of-agi" in line:
            line = line.replace(lnk, host_url + host_page + divagi)

    return line


# desired html
with open('index.html', 'w') as f:
    # write header info
    f.write(''.join(html_head))

    heavy_minus_tracker = 0
    all_lines = []
    table_of_contents = []
    dl_dnn = []
    ml_fund = []
    opt_ml = []
    gen_ml = []
    reinf_learn = []
    bayes_dl = []
    med_img = []
    prob_gm = []
    graph_nn = []
    nlp_nn = []
    asr_nn = []
    cv_nn = []
    bcss = []
    agi_nn = []
    for line in markdn:
        if line.startswith('# '):
            line = line.replace('# ', '')
            # very first line
            if ":" in line:
                temp = []
                line_contents = line.split(" ")
                for w in line_contents:
                    if ":" in w:
                        continue  # comment this line to enable emoji
                        w = w.replace(":", "")
                        w = prettify_emoji(w)
                        temp.append(w)
                    else:
                        temp.append(w)
                line = " ".join(temp)
                del temp
                line = h1b + fontawesome_animations[0] + line + fontawesome_animations[1] + h1e
                all_lines.append(line)
                # line separator
                all_lines.append('<hr>')

        # quote
        if ":books:" in line:
            # extract URL/text
            extracted = parse_markdown_url(line)
            line = convert_markdown_url2html(line, extracted)

            # line = line.replace(lb_html, '')  # remove line break
            line = line.replace(":books:", prettify_emoji("books"))  # color code emoji
            line = line.replace('**"', '<strong>"')  # bold text
            line = line.replace('"**', '"</strong>')
            all_lines.append(line)

        # if heavy minus, just pass
        if ":heavy_minus_sign:" in line:
            heavy_minus_tracker += 1
            continue

        # table of contents
        if "### Contents" in line:
            line = line.replace('### ', '')
            line = '<div id="contents"> ' + ahref1 + host_page + divcont + ahrefm + h2b + line + h2e + ahref2
            line = line + ' </div>'
            # print(line)
            all_lines.append(line)

        # group toc in a list and then process them
        if "| " in line and heavy_minus_tracker == 2:
            line = line.replace(down_arrow, down_arrow_prettified)
            extr = parse_markdown_url(line)
            matches = re.findall(r"\(https.*?\)", line)
            line = replace_github_url_with_webpage_url(line, matches)
            table_of_contents.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 3:
            # convert toc markdown to html table
            toc_html = markdown.markdown("".join(table_of_contents), extensions=['markdown.extensions.tables'])
            toc_html = toc_html.replace('<table>', '<table id="toc" class="centerTable">')  # center align table
            all_lines.append(toc_html)
            all_lines.append('<br/> <br/>')
            all_lines.append('<hr>')

        # Depp Neurl Networks TABLE
        # table Deep Learning (Deep Neural Networks)
        if "## :tada: Deep Learning" in line:
            line = line.replace('## ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + host_page + divdnns + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

        # group DNN table in a list and then process them
        if "| " in line and heavy_minus_tracker == 4:
            dl_dnn.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 5:
            # convert DL DNN markdown to html table
            dl_dnn_html = markdown.markdown("".join(dl_dnn), extensions=['markdown.extensions.tables'])
            dl_dnn_html = dl_dnn_html.replace('<table>', '<table id="dldnn">')  # center align table
            # remove underline in url links
            dl_dnn_html = dl_dnn_html.replace('">', '" style="text-decoration:none">')
            # print(dl_dnn_html)
            all_lines.append(dl_dnn_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # ML FUNDAMENTALS TABLE
        # ML fundamentals
        if "### :cupid: Machine Learning" in line:
            line = line.replace('### ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divmlfund + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

         # group ML fundamentals table in a list and then process them
        if "| " in line and heavy_minus_tracker == 6:
            ml_fund.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 7:
            # convert ML Funda markdown to html table
            ml_fund_html = markdown.markdown("".join(ml_fund), extensions=['markdown.extensions.tables'])
            ml_fund_html = ml_fund_html.replace('<table>', '<table id="mlfund">')  # center align table
            # remove underline in url links
            ml_fund_html = ml_fund_html.replace('">', '" style="text-decoration:none">')
            # print(ml_fund_html)
            all_lines.append(ml_fund_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # OPT for ML TABLE
        # Optimization for Machine Learning
        if "### :cupid: Optimization for Machine Learning" in line:
            line = line.replace('### ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divopt4ml + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

         # group OPT 4 ML table in a list and then process them
        if "| " in line and heavy_minus_tracker == 8:
            opt_ml.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 9:
            # convert Optim 4 ML markdown to html table
            opt_ml_html = markdown.markdown("".join(opt_ml), extensions=['markdown.extensions.tables'])
            opt_ml_html = opt_ml_html.replace('<table>', '<table id="opt4ml">')  # center align table
            # remove underline in url links
            opt_ml_html = opt_ml_html.replace('">', '" style="text-decoration:none">')
            # print(opt_ml_html)
            all_lines.append(opt_ml_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # GENERAL ML TABLE
        # General Machine Learning
        if "### :cupid: General Machine" in line:
            line = line.replace('### ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divgenml + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

        # group General ML table in a list and then process them
        if "| " in line and heavy_minus_tracker == 10:
            gen_ml.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 11:
            # convert General ML markdown to html table
            gen_ml_html = markdown.markdown("".join(gen_ml), extensions=['markdown.extensions.tables'])
            gen_ml_html = gen_ml_html.replace('<table>', '<table id="genml">')  # center align table
            # remove underline in url links
            gen_ml_html = gen_ml_html.replace('">', '" style="text-decoration:none">')
            # print(gen_ml_html)
            all_lines.append(gen_ml_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # REINFORCEMENT LEARNING TABLE
        # Reinforcement Learning
        if "### :balloon: Reinforcement" in line:
            line = line.replace('### ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divreinf + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

        # group Reinforcement Learning table in a list and then process them
        if "| " in line and heavy_minus_tracker == 12:
            reinf_learn.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 13:
            # convert reinforce learn markdown to html table
            reinf_learn_html = markdown.markdown("".join(reinf_learn), extensions=['markdown.extensions.tables'])
            reinf_learn_html = reinf_learn_html.replace('<table>', '<table id="reinf">')  # center align table
            # remove underline in url links
            reinf_learn_html = reinf_learn_html.replace('">', '" style="text-decoration:none">')
            # print(reinf_learn_html)
            all_lines.append(reinf_learn_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # PROBABILISTIC GRAPHICAL MODELS TABLE
        # Probabilistic Graphical Models
        if "### :loudspeaker: Probabilistic Graphical Models" in line:
            line = line.replace('### ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divpgm + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

        # group Probabilistic Graphical Models table in a list and then process them
        if "| " in line and heavy_minus_tracker == 14:
            prob_gm.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 15:
            # convert Probabilistic Graphical Models markdown to html table
            prob_gm_html = markdown.markdown("".join(prob_gm), extensions=['markdown.extensions.tables'])
            prob_gm_html = prob_gm_html.replace('<table>', '<table id="probgm">')  # center align table
            # remove underline in url links
            prob_gm_html = prob_gm_html.replace('">', '" style="text-decoration:none">')
            # print(prob_gm_html)
            all_lines.append(prob_gm_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # BAYESIAN DEEP LEARNING TABLE
        # Bayesian Deep Learning
        if "## :game_die: Bayesian" in line:
            line = line.replace('## ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divbdl + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

        # group Bayesian Deep Learning table in a list and then process them
        if "| " in line and heavy_minus_tracker == 16:
            bayes_dl.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 17:
            # convert bayes deep learn markdown to html table
            bayes_dl_html = markdown.markdown("".join(bayes_dl), extensions=['markdown.extensions.tables'])
            bayes_dl_html = bayes_dl_html.replace('<table>', '<table id="bayesdl">')  # center align table
            # remove underline in url links
            reinf_learn_html = bayes_dl_html.replace('">', '" style="text-decoration:none">')
            # print(bayes_dl_html)
            all_lines.append(bayes_dl_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # MEDICAL IMAGING TABLE
        # Medical Imaging
        if "## :movie_camera: Medical" in line:
            line = line.replace('## ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divmi + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

        # group Medical Imaging table in a list and then process them
        if "| " in line and heavy_minus_tracker == 18:
            med_img.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 19:
            # convert medical imaging markdown to html table
            med_img_html = markdown.markdown("".join(med_img), extensions=['markdown.extensions.tables'])
            med_img_html = med_img_html.replace('<table>', '<table id="medimg">')  # center align table
            # remove underline in url links
            med_img_html = med_img_html.replace('">', '" style="text-decoration:none">')
            # print(med_img_html)
            all_lines.append(med_img_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # GRAPH NEURAL NETWORKS TABLE
        # Graph Neural Networks
        if "## :tada: Graph Neural Networks" in line:
            line = line.replace('## ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divgnn + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

        # group Graph Neural Networks table in a list and then process them
        if "| " in line and heavy_minus_tracker == 20:
            graph_nn.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 21:
            # convert Graph Neural Networks markdown to html table
            graph_nn_html = markdown.markdown("".join(graph_nn), extensions=['markdown.extensions.tables'])
            graph_nn_html = graph_nn_html.replace('<table>', '<table id="graphnn">')  # center align table
            # remove underline in url links
            graph_nn_html = graph_nn_html.replace('">', '" style="text-decoration:none">')
            # print(graph_nn_html)
            all_lines.append(graph_nn_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # NATURAL LANGUAGE PROCESSING TABLE
        # Natural Language Processing
        if "### :hibiscus: Natural Language Processing" in line:
            line = line.replace('### ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divnlp + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

        # group Natural Language Processing table in a list and then process them
        if "| " in line and heavy_minus_tracker == 22:
            nlp_nn.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 23:
            # convert Graph Neural Networks markdown to html table
            nlp_nn_html = markdown.markdown("".join(nlp_nn), extensions=['markdown.extensions.tables'])
            nlp_nn_html = nlp_nn_html.replace('<table>', '<table id="nlpnn">')  # center align table
            # remove underline in url links
            nlp_nn_html = nlp_nn_html.replace('">', '" style="text-decoration:none">')
            # print(nlp_nn_html)
            all_lines.append(nlp_nn_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # Automatic Speech Recognition TABLE
        # Automatic Speech Recognition
        if "###  :speaking_head: Automatic Speech Recognition" in line:
            line = line.replace('### ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divasr + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

        # group Automatic Speech Recognition table in a list and then process them
        if "| " in line and heavy_minus_tracker == 24:
            asr_nn.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 25:
            # convert Automatic Speech Recognition markdown to html table
            asr_nn_html = markdown.markdown("".join(asr_nn), extensions=['markdown.extensions.tables'])
            asr_nn_html = asr_nn_html.replace('<table>', '<table id="asrnn">')  # center align table
            # remove underline in url links
            asr_nn_html = asr_nn_html.replace('">', '" style="text-decoration:none">')
            # print(asr_nn_html)
            all_lines.append(asr_nn_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # Modern Computer Vision TABLE
        # Modern Computer Vision
        if "### :fire: Modern Computer Vision" in line:
            line = line.replace('### ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divcvnn + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

        # group Modern Computer Vision table in a list and then process them
        if "| " in line and heavy_minus_tracker == 26:
            cv_nn.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 27:
            # convert Modern Computer Vision markdown to html table
            cv_nn_html = markdown.markdown("".join(cv_nn), extensions=['markdown.extensions.tables'])
            cv_nn_html = cv_nn_html.replace('<table>', '<table id="cvnn">')  # center align table
            # remove underline in url links
            cv_nn_html = cv_nn_html.replace('">', '" style="text-decoration:none">')
            # print(cv_nn_html)
            all_lines.append(cv_nn_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # Boot Camps or Summer Schools TABLE
        # Boot Camps or Summer Schools
        if "### :star2: Boot Camps or Summer Schools" in line:
            line = line.replace('### ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divbcss + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

        # group Boot Camps or Summer Schools table in a list and then process them
        if "| " in line and heavy_minus_tracker == 28:
            bcss.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 29:
            # convert Boot Camps or Summer Schools markdown to html table
            bcss_html = markdown.markdown("".join(bcss), extensions=['markdown.extensions.tables'])
            bcss_html = bcss_html.replace('<table>', '<table id="bcss">')  # center align table
            # remove underline in url links
            bcss_html = bcss_html.replace('">', '" style="text-decoration:none">')
            # print(bcss_html)
            all_lines.append(bcss_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

        # Bird's Eye view of A(G)I TABLE
        # Bird's Eye view of A(G)I
        if "### :bird: Bird" in line:
            line = line.replace('### ', '')
            line = table_topic_emoji_processor(line)
            line = ahref1 + divagi + ahrefm + h2b + line + h2e + ahref2
            # print(line)
            all_lines.append(line)

        # group Bird's Eye view of A(G)I table in a list and then process them
        if "| " in line and heavy_minus_tracker == 30:
            agi_nn.append(line)

        # signifies end of table; now convert them to html table
        if heavy_minus_tracker == 31:
            # convert Bird's Eye view of A(G)I markdown to html table
            agi_nn_html = markdown.markdown("".join(agi_nn), extensions=['markdown.extensions.tables'])
            agi_nn_html = agi_nn_html.replace('<table>', '<table id="aginn">')  # center align table
            # remove underline in url links
            agi_nn_html = agi_nn_html.replace('">', '" style="text-decoration:none">')
            # print(agi_nn_html)
            all_lines.append(agi_nn_html)

            # navigation to top
            all_lines.append(add_navigation_button())
            all_lines.append("<hr>")

    # write everything to desired html file
    for line in all_lines:
        f.write(line)

    # write footer info
    f.write(''.join(html_foot))
