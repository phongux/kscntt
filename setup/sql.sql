PGDMP         '            	    w            im    12.0    12.0 J    {           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            |           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            }           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            ~           1262    16393    im    DATABASE     �   CREATE DATABASE im WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';
    DROP DATABASE im;
                postgres    false            �            1259    16396    account    TABLE        CREATE TABLE public.account (
    id bigint NOT NULL,
    username text,
    email text,
    account_password text,
    account_level integer,
    team text,
    fullname text,
    update_time timestamp without time zone DEFAULT now(),
    captcha text
);
    DROP TABLE public.account;
       public         heap    postgres    false            �            1259    16394    account_id_seq    SEQUENCE     w   CREATE SEQUENCE public.account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.account_id_seq;
       public          postgres    false    203                       0    0    account_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.account_id_seq OWNED BY public.account.id;
          public          postgres    false    202            �            1259    16408    admin_first_menu    TABLE     �   CREATE TABLE public.admin_first_menu (
    id bigint NOT NULL,
    fid integer,
    menu1 text,
    link text,
    update_time timestamp without time zone DEFAULT now()
);
 $   DROP TABLE public.admin_first_menu;
       public         heap    postgres    false            �            1259    16406    admin_first_menu_id_seq    SEQUENCE     �   CREATE SEQUENCE public.admin_first_menu_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.admin_first_menu_id_seq;
       public          postgres    false    205            �           0    0    admin_first_menu_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.admin_first_menu_id_seq OWNED BY public.admin_first_menu.id;
          public          postgres    false    204            �            1259    16420    admin_second_menu    TABLE     �   CREATE TABLE public.admin_second_menu (
    id bigint NOT NULL,
    first_menu_id integer,
    menu2 text,
    link text,
    update_time timestamp without time zone DEFAULT now()
);
 %   DROP TABLE public.admin_second_menu;
       public         heap    postgres    false            �            1259    16418    admin_second_menu_id_seq    SEQUENCE     �   CREATE SEQUENCE public.admin_second_menu_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.admin_second_menu_id_seq;
       public          postgres    false    207            �           0    0    admin_second_menu_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.admin_second_menu_id_seq OWNED BY public.admin_second_menu.id;
          public          postgres    false    206            �            1259    16432 
   first_menu    TABLE     �   CREATE TABLE public.first_menu (
    id bigint NOT NULL,
    fid integer,
    menu1 text,
    link text,
    update_time timestamp without time zone DEFAULT now()
);
    DROP TABLE public.first_menu;
       public         heap    postgres    false            �            1259    16430    first_menu_id_seq    SEQUENCE     z   CREATE SEQUENCE public.first_menu_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.first_menu_id_seq;
       public          postgres    false    209            �           0    0    first_menu_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.first_menu_id_seq OWNED BY public.first_menu.id;
          public          postgres    false    208            �            1259    16480    most_used_table    TABLE     �   CREATE TABLE public.most_used_table (
    id bigint NOT NULL,
    tablename text,
    sqlcreated text,
    update_time timestamp without time zone DEFAULT now()
);
 #   DROP TABLE public.most_used_table;
       public         heap    postgres    false            �            1259    16478    most_used_table_id_seq    SEQUENCE        CREATE SEQUENCE public.most_used_table_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.most_used_table_id_seq;
       public          postgres    false    217            �           0    0    most_used_table_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.most_used_table_id_seq OWNED BY public.most_used_table.id;
          public          postgres    false    216            �            1259    16468    querysql    TABLE     �   CREATE TABLE public.querysql (
    id bigint NOT NULL,
    dowhat text,
    querysql text,
    detail text,
    update_time timestamp without time zone DEFAULT now()
);
    DROP TABLE public.querysql;
       public         heap    postgres    false            �            1259    16466    querysql_id_seq    SEQUENCE     x   CREATE SEQUENCE public.querysql_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.querysql_id_seq;
       public          postgres    false    215            �           0    0    querysql_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.querysql_id_seq OWNED BY public.querysql.id;
          public          postgres    false    214            �            1259    16444    second_menu    TABLE     �   CREATE TABLE public.second_menu (
    id bigint NOT NULL,
    first_menu_id integer,
    menu2 text,
    link text,
    update_time timestamp without time zone DEFAULT now()
);
    DROP TABLE public.second_menu;
       public         heap    postgres    false            �            1259    16442    second_menu_id_seq    SEQUENCE     {   CREATE SEQUENCE public.second_menu_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.second_menu_id_seq;
       public          postgres    false    211            �           0    0    second_menu_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.second_menu_id_seq OWNED BY public.second_menu.id;
          public          postgres    false    210            �            1259    16504    service_manager    TABLE     �   CREATE TABLE public.service_manager (
    id bigint NOT NULL,
    file text,
    service text,
    note text,
    update_time timestamp without time zone DEFAULT now()
);
 #   DROP TABLE public.service_manager;
       public         heap    postgres    false            �            1259    16502    service_manager_id_seq    SEQUENCE        CREATE SEQUENCE public.service_manager_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.service_manager_id_seq;
       public          postgres    false    221            �           0    0    service_manager_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.service_manager_id_seq OWNED BY public.service_manager.id;
          public          postgres    false    220            �            1259    16492    settings    TABLE     �   CREATE TABLE public.settings (
    id bigint NOT NULL,
    tablename text,
    dowhat text,
    query text,
    sqlcraeted text,
    detail text,
    update_time timestamp without time zone DEFAULT now()
);
    DROP TABLE public.settings;
       public         heap    postgres    false            �            1259    16490    settings_id_seq    SEQUENCE     x   CREATE SEQUENCE public.settings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.settings_id_seq;
       public          postgres    false    219            �           0    0    settings_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.settings_id_seq OWNED BY public.settings.id;
          public          postgres    false    218            �            1259    16456    user_report    TABLE     �   CREATE TABLE public.user_report (
    id bigint NOT NULL,
    agent text,
    gmail text,
    update_time timestamp without time zone DEFAULT now()
);
    DROP TABLE public.user_report;
       public         heap    postgres    false            �            1259    16454    user_report_id_seq    SEQUENCE     {   CREATE SEQUENCE public.user_report_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.user_report_id_seq;
       public          postgres    false    213            �           0    0    user_report_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.user_report_id_seq OWNED BY public.user_report.id;
          public          postgres    false    212            �
           2604    16399 
   account id    DEFAULT     h   ALTER TABLE ONLY public.account ALTER COLUMN id SET DEFAULT nextval('public.account_id_seq'::regclass);
 9   ALTER TABLE public.account ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    202    203    203            �
           2604    16411    admin_first_menu id    DEFAULT     z   ALTER TABLE ONLY public.admin_first_menu ALTER COLUMN id SET DEFAULT nextval('public.admin_first_menu_id_seq'::regclass);
 B   ALTER TABLE public.admin_first_menu ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    205    204    205            �
           2604    16423    admin_second_menu id    DEFAULT     |   ALTER TABLE ONLY public.admin_second_menu ALTER COLUMN id SET DEFAULT nextval('public.admin_second_menu_id_seq'::regclass);
 C   ALTER TABLE public.admin_second_menu ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    206    207    207            �
           2604    16435    first_menu id    DEFAULT     n   ALTER TABLE ONLY public.first_menu ALTER COLUMN id SET DEFAULT nextval('public.first_menu_id_seq'::regclass);
 <   ALTER TABLE public.first_menu ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    208    209    209            �
           2604    16483    most_used_table id    DEFAULT     x   ALTER TABLE ONLY public.most_used_table ALTER COLUMN id SET DEFAULT nextval('public.most_used_table_id_seq'::regclass);
 A   ALTER TABLE public.most_used_table ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    217    217            �
           2604    16471    querysql id    DEFAULT     j   ALTER TABLE ONLY public.querysql ALTER COLUMN id SET DEFAULT nextval('public.querysql_id_seq'::regclass);
 :   ALTER TABLE public.querysql ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214    215            �
           2604    16447    second_menu id    DEFAULT     p   ALTER TABLE ONLY public.second_menu ALTER COLUMN id SET DEFAULT nextval('public.second_menu_id_seq'::regclass);
 =   ALTER TABLE public.second_menu ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    211    210    211            �
           2604    16507    service_manager id    DEFAULT     x   ALTER TABLE ONLY public.service_manager ALTER COLUMN id SET DEFAULT nextval('public.service_manager_id_seq'::regclass);
 A   ALTER TABLE public.service_manager ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    221    221            �
           2604    16495    settings id    DEFAULT     j   ALTER TABLE ONLY public.settings ALTER COLUMN id SET DEFAULT nextval('public.settings_id_seq'::regclass);
 :   ALTER TABLE public.settings ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    218    219            �
           2604    16459    user_report id    DEFAULT     p   ALTER TABLE ONLY public.user_report ALTER COLUMN id SET DEFAULT nextval('public.user_report_id_seq'::regclass);
 =   ALTER TABLE public.user_report ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    213    212    213            f          0    16396    account 
   TABLE DATA           }   COPY public.account (id, username, email, account_password, account_level, team, fullname, update_time, captcha) FROM stdin;
    public          postgres    false    203   �Q       h          0    16408    admin_first_menu 
   TABLE DATA           M   COPY public.admin_first_menu (id, fid, menu1, link, update_time) FROM stdin;
    public          postgres    false    205   �S       j          0    16420    admin_second_menu 
   TABLE DATA           X   COPY public.admin_second_menu (id, first_menu_id, menu2, link, update_time) FROM stdin;
    public          postgres    false    207   �S       l          0    16432 
   first_menu 
   TABLE DATA           G   COPY public.first_menu (id, fid, menu1, link, update_time) FROM stdin;
    public          postgres    false    209   NT       t          0    16480    most_used_table 
   TABLE DATA           Q   COPY public.most_used_table (id, tablename, sqlcreated, update_time) FROM stdin;
    public          postgres    false    217   �T       r          0    16468    querysql 
   TABLE DATA           M   COPY public.querysql (id, dowhat, querysql, detail, update_time) FROM stdin;
    public          postgres    false    215   �T       n          0    16444    second_menu 
   TABLE DATA           R   COPY public.second_menu (id, first_menu_id, menu2, link, update_time) FROM stdin;
    public          postgres    false    211   =U       x          0    16504    service_manager 
   TABLE DATA           O   COPY public.service_manager (id, file, service, note, update_time) FROM stdin;
    public          postgres    false    221   �U       v          0    16492    settings 
   TABLE DATA           a   COPY public.settings (id, tablename, dowhat, query, sqlcraeted, detail, update_time) FROM stdin;
    public          postgres    false    219   �U       p          0    16456    user_report 
   TABLE DATA           D   COPY public.user_report (id, agent, gmail, update_time) FROM stdin;
    public          postgres    false    213   lV       �           0    0    account_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.account_id_seq', 1, true);
          public          postgres    false    202            �           0    0    admin_first_menu_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.admin_first_menu_id_seq', 1, true);
          public          postgres    false    204            �           0    0    admin_second_menu_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.admin_second_menu_id_seq', 1, true);
          public          postgres    false    206            �           0    0    first_menu_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.first_menu_id_seq', 2, true);
          public          postgres    false    208            �           0    0    most_used_table_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.most_used_table_id_seq', 1, true);
          public          postgres    false    216            �           0    0    querysql_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.querysql_id_seq', 1, true);
          public          postgres    false    214            �           0    0    second_menu_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.second_menu_id_seq', 2, true);
          public          postgres    false    210            �           0    0    service_manager_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.service_manager_id_seq', 1, false);
          public          postgres    false    220            �           0    0    settings_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.settings_id_seq', 6, true);
          public          postgres    false    218            �           0    0    user_report_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.user_report_id_seq', 1, true);
          public          postgres    false    212            �
           2606    16405    account account_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.account DROP CONSTRAINT account_pkey;
       public            postgres    false    203            �
           2606    16417 &   admin_first_menu admin_first_menu_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.admin_first_menu
    ADD CONSTRAINT admin_first_menu_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.admin_first_menu DROP CONSTRAINT admin_first_menu_pkey;
       public            postgres    false    205            �
           2606    16429 (   admin_second_menu admin_second_menu_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.admin_second_menu
    ADD CONSTRAINT admin_second_menu_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.admin_second_menu DROP CONSTRAINT admin_second_menu_pkey;
       public            postgres    false    207            �
           2606    16441    first_menu first_menu_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.first_menu
    ADD CONSTRAINT first_menu_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.first_menu DROP CONSTRAINT first_menu_pkey;
       public            postgres    false    209            �
           2606    16489 $   most_used_table most_used_table_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.most_used_table
    ADD CONSTRAINT most_used_table_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.most_used_table DROP CONSTRAINT most_used_table_pkey;
       public            postgres    false    217            �
           2606    16477    querysql querysql_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.querysql
    ADD CONSTRAINT querysql_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.querysql DROP CONSTRAINT querysql_pkey;
       public            postgres    false    215            �
           2606    16453    second_menu second_menu_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.second_menu
    ADD CONSTRAINT second_menu_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.second_menu DROP CONSTRAINT second_menu_pkey;
       public            postgres    false    211            �
           2606    16513 $   service_manager service_manager_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.service_manager
    ADD CONSTRAINT service_manager_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.service_manager DROP CONSTRAINT service_manager_pkey;
       public            postgres    false    221            �
           2606    16501    settings settings_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.settings DROP CONSTRAINT settings_pkey;
       public            postgres    false    219            �
           2606    16465    user_report user_report_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.user_report
    ADD CONSTRAINT user_report_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.user_report DROP CONSTRAINT user_report_pkey;
       public            postgres    false    213            f   
  x��Y��@  �o=�\�N-T���(B;*�B:!E-
(*�~z�w�G\Vy=�^���0D�%���7Җ2����
(�	���h�5V<������CRs����P��DB�3�3�[@�P[�@�%�`S
jIiJeƔ���_@k��?|"�	�E�@2x�7�f�6X�q�;Ί\E镨�<w��D�⅚8��"AF��:�<��]���;���_�MgL_����!Z��ħ�}��y�/��=�zve�*2�<��)[�H?�j�t����1�|�LN����8Ȣ�^1Y�������mYB�0��fM�u9��f�;U:T�=Z����'�������.��x��k{�~��Vb������ic�Q��r��7��Cq��|疪�΀ox��6+W�U#�%�&(�I�����r���|�:=��յu��]{{{��Aq�Eq\�Y��Ƨ��%,u� Z�E8�$�}��my�Cşy��+���������M&-ݭ.=����ֲW�y�wS��?���?��%      h   8   x�3�4�tL���S�M�+�T�420��54�50S02�2��22�3�0�0����� �
      j   F   x�3�4�tL�����//N�����O��+)���OZ���)XX��X�s��qqq f�      l   [   x�3�4�-N-R�M�+�T�420��54�50S02�26�20�322�0��2�4���O�/-��//N�����ρ�1t�Y���r��qqq ��      t   2   x�3�,I-.���420��54�50S02�20�26Գ01015����� �v      r   2   x�3�,I-.��!#CK]C]3#+#+cC=SC�=... �X	)      n   i   x�3�4�t�x��3/C���
%�d*dg�?ܵ8�S��8=S?3W?9?��(?G?199�4�$>71/1=������R��@��L��������R�����܈+F��� �       x      x������ � �      v   �   x���A
�0@�u���!3��D�"і,�P���Х��}|4��2���Ӷ�ӌ����uN����� �Ok���@�Y�� lZw�VU�x�<�k$$1�\��\�Ǎ �`dP3����� �����h��tN�      p   2   x�3�,I-.���420��54�50S02�20�26Գ01015����� �v     