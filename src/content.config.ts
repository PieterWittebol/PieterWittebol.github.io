import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const photography = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/photography' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      date: z.coerce.date(),
      image: image(),
      tags: z.array(z.string()).default([]),
      location: z.string().optional(),
      camera: z.string().optional(),
      draft: z.boolean().default(false),
    }),
});

const woodworking = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/woodworking' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string(),
      date: z.coerce.date(),
      cover: image(),
      tags: z.array(z.string()).default([]),
      draft: z.boolean().default(false),
    }),
});

const assignmentSchema = z.object({
  role: z.string(),
  company: z.string(),
  period: z.string(),
  description: z.string().default(''),
});

const about = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/about' }),
  schema: z.object({
    name: z.string(),
    title: z.string(),
    experience: z.array(
      z.object({
        role: z.string(),
        company: z.string(),
        period: z.string(),
        description: z.string().default(''),
        assignments: z.array(assignmentSchema).default([]),
      }),
    ),
    education: z.array(
      z.object({
        degree: z.string(),
        institution: z.string(),
        period: z.string(),
      }),
    ),
    certifications: z.array(z.string()).default([]),
    skills: z.array(z.string()).default([]),
    languages: z.array(
      z.object({
        name: z.string(),
        level: z.string(),
      }),
    ),
  }),
});

export const collections = { photography, woodworking, about };
