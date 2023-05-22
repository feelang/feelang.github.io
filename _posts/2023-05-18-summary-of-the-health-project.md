---
layout: single
classes: wide
author_profile: true
title: Health 项目技术总结
comments: true
toc: true
date: 2023-05-18
categories: Frontend
---

好长一段时间没写前端，很多知识点都忘掉了，为了防止遗忘，趁着项目刚结束，赶紧总结一下。

## 邂逅 `Next.js`

这个项目用的是 `next.js`，也是 `react` 官方推荐的。今天才知道原来 react 已经升级改版，我之前掌握的技能早已过时。

* React 官方推荐入口 => [Start a New React Project](https://react.dev/learn/start-a-new-react-project)
* [Next.js](https://nextjs.org/)

第一次用 `next.js`，不了解技术细节，不过从使用感受来说，还不错，用起来很方便。

从官网简介可以看出，这是一个全栈框架：

> Next.js enables you to create full-stack Web applications by extending the latest React features, and integrating powerful Rust-based JavaScript tooling for the fastest builds.

根据已经掌握的 [antd](https://ant.design/components) 知识，很快就把第一个页面搞定了。

开始搞第二个页面时，我开始网上寻找 Router 解决方案，找到了 [React Router](https://reactrouter.com/en/main)。

发现这个框架也已经升级改版，而我只掌握了上一个版本的用法，所以就开始翻文档，学习新用法，但是内容实在太长了，读不下去。

顺便发现了 `next.js` 自身内置了路由模块——[API Routes](https://nextjs.org/docs/pages/building-your-application/routing/api-routes)。

继续翻文档，结果云里雾里，根本看不懂。

灵机一动，不如去看看视频教程，找到了 [Next.js App Router: Routing, Data Fetching, Caching](https://www.youtube.com/watch?v=gSSsZReIFRk)。

原来在 `next.js` 项目中，只需要在 `app` 目录下新建一个文件夹就可以自动生成路由，实在方便。

就这样新建了第二个页面。

然后开始使用 `antd` 的 `Form` 组件写页面。

## 老朋友 AntD

### 使用 `Form`

```tsx
<Form
    form={form}
    layout="vertical"
    onFinish={onFinish}
    onFinishFailed={onFinishFailed}
>
```

其中：
* `form={form}` 的 `form` 来自：`const [form] = Form.useForm()`
* `onFinish` 和 `onFinishFailed` 是两个函数

```typescript
 const onFinish = (values: any) => {
    console.log(values)
 }

 const onFinishFailed = (errorInfo: any) => {
    console.log(errorInfo)
 }
```

页面底部添加两个按钮：计算 & 重置。

```tsx
<Form.Item>
    <Space>
        <Button type="primary" htmlType="submit">计算</Button>
        <Button htmlType="reset">重置</Button>
    </Space>
</Form.Item>
```

其中 `<Space>` 一用，就不用单独设置边距了，非常方便。

这两个按钮的功能通过设置 `htmlType` 属性来实现，其他任何代码不需要。

### `Form.Item` 的联动校验

其中一个输入框要填写年龄，且是必填：

```tsx
<Form.Item label="1 年龄(age)" name="age"
    rules={[{ required: true, message: '请输入年龄' }]}
>
    <InputNumber placeholder="请输入年龄" min={18} max={100}
        onChange={setAge}
    />
</Form.Item>
```

利用 `setAge` 接收输入值：

```typescript
const [age, setAge] = useState<string | number | null>(null)
```

> 需要留意的是，`InputNumber` 的 `onChange` 属性的变量类型为 `string | number | null`。

第二个输入框也是年龄，但它的输入值必须小于 `age`：

```tsx
<Form.Item label="3.1 绝经年龄(age at menopause)"
           name="menopauseAge"
           dependencies={['age']}
           rules={[
               {
                   required: true,
                   message: '请输入年龄',
               },
               ({ getFieldValue }) => ({
                   validator(_, value) {
                       if (!value || getFieldValue('age') >= value) {
                           return Promise.resolve();
                       }
                       return Promise.reject(new Error(`绝经年龄不得大于当前年龄(${age})`));
                   },
               }),
           ]}
>
```

这个用法值得仔细记录一下。

先看 `dependencies` 的用法，官网介绍如下，简单明了。

> 当字段间存在依赖关系时使用。如果一个字段设置了 dependencies 属性。那么它所依赖的字段更新时，该字段将自动触发更新与校验。
> 一种常见的场景，就是注册用户表单的“密码”与“确认密码”字段。“确认密码”校验依赖于“密码”字段，设置 dependencies 后，“密码”字段更新会重新触发“校验密码”的校验逻辑。

再看 `rules` 用法：

> 校验规则，设置字段的校验逻辑。

类型为 `Rule[]`，是个数组。

`Rule` 定义如下：

```typescript
type Rule = RuleConfig | ((form: FormInstance) => RuleConfig);
```

可以看出，`Rule` 支持两种类型，所以上面代码中 `rules` 的第一个元素类型为 `RuleConfig`：

```typescript
{
    required: true,
    message: '请输入年龄',
},
```

第二个元素类型为 `((form: FormInstance) => RuleConfig)`，是个高阶函数。

```tsx
({ getFieldValue }) => ({
    validator(_, value) {
        if (!value || getFieldValue('age') >= value) {
            return Promise.resolve();
        }
        return Promise.reject(new Error(`绝经年龄不得大于当前年龄(${age})`));
    },
}),
```

由此可以推测出 `getFieldValue` 是 `FormInstance` 的一个属性，通过看源码可以证实：

```typescript
export interface FormInstance<Values = any> {
    getFieldValue: (name: NamePath) => StoreValue;
    getFieldsValue: (() => Values) & ((nameList: NamePath[] | true, filterFunc?: (meta: Meta) => boolean) => any);
    getFieldError: (name: NamePath) => string[];
    getFieldsError: (nameList?: NamePath[]) => FieldError[];
    getFieldWarning: (name: NamePath) => string[];
    isFieldsTouched: ((nameList?: NamePath[], allFieldsTouched?: boolean) => boolean) & ((allFieldsTouched?: boolean) => boolean);
    isFieldTouched: (name: NamePath) => boolean;
    isFieldValidating: (name: NamePath) => boolean;
    isFieldsValidating: (nameList: NamePath[]) => boolean;
    resetFields: (fields?: NamePath[]) => void;
    setFields: (fields: FieldData[]) => void;
    setFieldValue: (name: NamePath, value: any) => void;
    setFieldsValue: (values: RecursivePartial<Values>) => void;
    validateFields: ValidateFields<Values>;
    submit: () => void;
}
```

`validator` 也是一个高阶函数：

```typescript
type Validator = (rule: RuleObject, value: StoreValue, callback: (error?: string) => void) => Promise<void | any> | void;
```

返回值是一个 `Promise` 或 `void`。

通过以上分析，可以总结出：当两个 `Form.Item` 之间存在依赖时，可通过 `dependencies` 和 `rules` 属性设定依赖逻辑。

## TypeScript tips

### string => number

```typescript
// menopauseAge 是个 `string`
const menopauseAge = values.menopauseAge ? +values.menopauseAge : 0
```

### interface

```typescript
interface RiskResult {
    message: string,
    description: string,
    type: "success" | "warning" | "error" | "info"
}
```

用法：
```typescript
const results: RiskResult[] = [
    {
        message: '乳腺癌低风险',
        description: '请继续保持健康生活方式',
        type: 'success'
    },
]
```

```typescript
const [result, setResult] = useState<RiskResult>()
```

